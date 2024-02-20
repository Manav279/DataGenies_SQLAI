import os
import streamlit as st
from langchain_openai import OpenAI
from Resources.generate_graph_prompt import generate_prompt
from Resources.sqlserver_execute import execute_query

def main():
    #Streamlit Code
    st.set_page_config(page_title="Visualize", page_icon="📊")
    st.title("Visualize Queries")
    query = st.text_input("Enter Your Query")

    llm = OpenAI(temperature=0.9)

    prompt = generate_prompt(query)
    if prompt:
        response = llm(prompt=prompt)
        if "[/SQL]" in response:
            response = response.split("[/SQL]")[0]
        if "[END_SQL]" in response:
            response = response.split("[END_SQL]")[0]
        with st.expander(label="SQL Query",expanded=True):
            st.write(response)
        if response != "I do not know" or 'Cannot represent given query in graph':
            output_df = execute_query(response)
            data_tab, graph_tab2 = st.tabs(["🗃 Data", "📈 Chart"])
            data_tab.subheader("Output Data")
            data_tab.write(output_df)
            graph_tab2.subheader("Graph")
            x_col = output_df.columns[0]
            y_col = output_df.columns[1]
            graph_tab2.bar_chart(output_df, x=x_col, y=y_col)

    st.button("Re-Generate")

if __name__ == "__main__":
    main()
