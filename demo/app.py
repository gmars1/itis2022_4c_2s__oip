import time
import pandas as pd
import streamlit as st

from demo.engine_launcher import launch
from files_management.files_accessor import FilesAccessor
# Импортируем твои новые модули
from styles import apply_custom_styles 

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(
    page_title="Поиск по документам",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_custom_styles()

# --- ЗАГРУЗКА ДАННЫХ ---
@st.cache_resource
def get_resources():
    """Единая точка инициализации тяжелых ресурсов"""
    try:
        engines = launch()  # Теперь возвращает Dict[str, Engine]
        doc_texts = dict()
        files = FilesAccessor()
        files.get_text_from_docs(doc_texts)
        index: dict[int, str] = files.get_index()
        return engines, doc_texts, index
    except Exception as e:
        st.error(f"❌ Критическая ошибка инициализации: {e}")
        st.stop()

engines, docs, links_index = get_resources()

# --- ИНИЦИАЛИЗАЦИЯ STATE ---
if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_time" not in st.session_state:
    st.session_state.search_time = None

# --- БОКОВАЯ ПАНЕЛЬ (SIDEBAR) ---
with st.sidebar:
    st.title("Настройки")
    
    st.divider()
    
    # ВЫБОР ДВИЖКА
    selected_engine_name = st.radio(
        "Способ поиска",
        options=list(engines.keys()),
        horizontal=False  # можно сделать горизонтально
    )
    current_engine = engines[selected_engine_name]

    st.divider()

    top_k = st.slider(
        "Количество результатов",
        min_value=1, max_value=20, value=5
    )

    st.divider()

    if st.button("🔄 Сбросить всё", use_container_width=True):
        st.session_state.search_results = None
        st.session_state.search_query = ""
        st.rerun()

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.markdown("<h1 class='main-header'>🔍 Поиск по документам</h1>", unsafe_allow_html=True)

with st.form("search_form", clear_on_submit=False):
    col1, col2 = st.columns([4, 1])

    with col1:
        query = st.text_input(
            "🔎 Запрос:",
            value=st.session_state.search_query,
            placeholder="Что ищем?",
            key="search_input"
        )

    with col2:
        st.write("")
        search_clicked = st.form_submit_button(
            "Найти",
            type="primary",
            use_container_width=True
        )
        
# --- ЛОГИКА ПОИСКА ---
if search_clicked and query:
    with st.spinner(f"🔄 {selected_engine_name} ищет..."):
        try:
            start_t = time.time()
            
            # Вызов метода конкретного выбранного движка
            doc_scores = current_engine.get_docs(query) or []
            
            final_docs = doc_scores[:top_k]
            
            st.session_state.search_time = time.time() - start_t
            st.session_state.search_results = [
                {
                    "id": doc_id,
                    "score": score,
                    "text": docs.get(doc_id, "Текст не найден")
                }
                for doc_id, score in final_docs
            ]
            st.session_state.search_query = query
        except Exception as e:
            st.error(f"Ошибка поиска: {e}")

# --- РЕНДЕРИНГ РЕЗУЛЬТАТОВ ---
if st.session_state.search_results is not None:
    res = st.session_state.search_results
    if res:
        st.info(f"⏱ Найдено {len(res)} док. за {st.session_state.search_time:.3f} сек.")
        
        for idx, item in enumerate(res, 1):
            with st.container():
                
                st.markdown(f"""
                <a href="{links_index[item['id']]}" target="_blank" style="text-decoration: none; color: inherit;">
                    <span class='score-badge'>#{idx}</span>
                    <span style="margin-left: 10px;">id: `{item['id']}`  |  Score: `{item['score']:.4f}`</span>
                </a>
                """, unsafe_allow_html=True)
                
                
                txt = item['text']
                st.write(txt[:450] + "..." if len(txt) > 450 else txt)
        
                with st.expander("📖 Полный текст"):
                    st.write(item['text'])
        
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Ничего не найдено.")
else:
    # Приветственный экран
    st.info("👋 Введите запрос.")

# Опционально: таблица всех данных
# with st.sidebar.expander("📊 Просмотр базы"):
#     st.write(pd.DataFrame(list(docs.items()), columns=["ID", "Text"]).head(10))