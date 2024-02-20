import os
import streamlit as st

os.environ["OPENAI_API_KEY"] = "[YOUR_OPEN_AI_API_KEY]"

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to  SQL AI! 👋")

st.markdown(
    """
    SQL AI is a Generative-AI Application designed to interface with your database, 
    transforming natural language prompts into SQL queries.\n
    **👈 Select an option from the sidebar** explore your Database!
"""
)

# python -m streamlit run .\SQLAI.py