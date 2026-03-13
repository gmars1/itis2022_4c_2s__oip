import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        .main-header { font-size: 2.5rem; color: #FF4B4B; text-align: center; margin-bottom: 2rem; }
        .result-card { background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; 
                      margin-bottom: 1rem; border-left: 4px solid #FF4B4B; }
        .score-badge { background-color: #FF4B4B; color: white; padding: 0.2rem 0.8rem; 
                      border-radius: 1rem; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)