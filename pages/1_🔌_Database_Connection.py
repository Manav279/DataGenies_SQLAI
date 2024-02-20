import os
import streamlit as st

st.set_page_config(page_title="Database Connection", page_icon="🔌")

st.title("Database Connection")
st.markdown("Enter Your Database Credentials:")
server = st.text_input("Server Address")
database = st.text_input("Database Name")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Save"):
    os.environ["SERVER_ADDRESS"] = server
    os.environ["DATABASE_NAME"] = database
    os.environ["DB_USERNAME"] = username
    os.environ["DB_PASSWORD"] = password