import os
from langchain_openai import OpenAI
import streamlit as st
from Resources.generate_prompt_schema import generate_prompt
from Resources.sqlserver_execute import execute_query

def main():

    #frontend
    st.set_page_config(page_title="SQL Query Generator", page_icon="📋")

    st.title("SQL Query Generator")
    prompt = st.text_input("Enter your Query")

    #prompt_template = load_prompt(f"{root_dir}/prompts/tpch_prompt.yaml")
    #final_prompt = prompt_template.format(input=prompt)
    final_prompt = generate_prompt(prompt)


    llm = OpenAI(temperature=0.9)

    if prompt:
        response = llm(prompt=final_prompt)
        if "[/SQL]" in response:
            response = response.split("[/SQL]")[0]
        with st.expander(label="SQL Query",expanded=True):
            st.write(response)
        if response != "I do not know":
            output = execute_query(response)
            st.write(output)

    st.button("Re-Generate")


if __name__ == "__main__":
    main()
