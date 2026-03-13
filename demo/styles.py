import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* Заголовок */
        .main-header { 
            font-size: 2.5rem; 
            color: #FF4B4B; 
            text-align: center; 
            margin-bottom: 2rem; 
        }
        
        .score-badge { 
            background-color: #FF4B4B; 
            color: white; 
            padding: 0.2rem 0.8rem; 
            border-radius: 1rem; 
            font-weight: bold; 
            display: inline-block; 
            min-width: 2rem;
            text-align: center;
        }
        
    </style>
    """, unsafe_allow_html=True)