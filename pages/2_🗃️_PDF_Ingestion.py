import streamlit as st
from Resources.extract_pdf import create_docs


def main():

    st.set_page_config(page_title="PDF Ingestion", page_icon="🗃️")

    st.title("Invoice Extraction Bot...💁 ")
    st.subheader("I can help you in extracting invoice data")


    # Upload the Invoices (pdf files)...
    pdf = st.file_uploader("Upload invoices here, only PDF files allowed", type=["pdf"],accept_multiple_files=True)

    submit=st.button("Extract Data")

    if submit:
        with st.spinner('Wait for it...'):
            df=create_docs(pdf)
            st.write(df)
            data_as_csv= df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download data as CSV", 
                data_as_csv, 
                "benchmark-tools.csv",
                "text/csv",
                key="download-tools-csv",
            )
        st.success("Hope I was able to save your time❤️")


#Invoking main function
if __name__ == '__main__':
    main()
