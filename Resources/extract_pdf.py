import os
from langchain_openai import OpenAI
from pypdf import PdfReader
from langchain_openai import OpenAI
import pandas as pd
import pymssql
import re
from langchain.prompts import PromptTemplate

conn = pymssql.connect(
    server=os.environ["SERVER_ADDRESS"],
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE_NAME"],
    as_dict=True
)  

print(conn)
print("connection established")

#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

#Function to extract data from text
def extracted_data(pages_data):

    template = """Extract all the following values : Invoice_no, Order_ID, Bill_to:, Ship To:, Date, Ship Mode:, Item, Quantity, Rate, Amount, Subtotal, Discount, Shipping, Total from this data: {pages}

        Expected output: remove any dollar symbols {{'Invoice_no': 30845, 'Order_ID': 'ID-2012-AH100757-41163', 'Bill_to': 'Adam Hart', 'Ship_To':'Melton, Victoria,Australia', 'Date': '2012 Sep 11','Ship_Mode':'Second Class', 'Item':'Konica Inkjet, White, Machines, Technology, TEC-MA-5007','Quantity': 4, 'Rate': 745.42, 'Amount': 2981.66,'Subtotal':2981.66,'Discount':1192.66, 'Shipping': 77.95, 'Total': 1866.95}}
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    llm = OpenAI(temperature=.7)
    full_response=llm(prompt_template.format(pages=pages_data))
    
    return full_response


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list):
    
    df = pd.DataFrame({
                    'Invoice_no': pd.Series(dtype='str'),
                    'Order_ID': pd.Series(dtype='str'),
                    'Bill_to': pd.Series(dtype='str'),
                    'Ship_To': pd.Series(dtype='str'),
                    'Date': pd.Series(dtype='str'),
                    'Ship_Mode': pd.Series(dtype='str'),
                    'Item': pd.Series(dtype='str'),
                    'Quantity': pd.Series(dtype='str'),
                    'Rate': pd.Series(dtype='str'),
                    'Amount': pd.Series(dtype='str'),
                    'Subtotal': pd.Series(dtype='str'),
                    'Discount': pd.Series(dtype='str'),
                    'Shipping': pd.Series(dtype='str'),
                    'Total': pd.Series(dtype='str')
                    })
    cursor = conn.cursor()

    for filename in user_pdf_list:
        
        print(filename)
        raw_data=get_pdf_text(filename)

        llm_extracted_data=extracted_data(raw_data)
        #Adding items to our list - Adding data & its metadata

        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            print(extracted_text)
            # Converting the extracted text to a dictionary
            data_dict = eval('{' + extracted_text + '}')
            columns_list = ['Invoice_no', 'Order_ID', 'Customer_Name', 'Address','Date', 'Ship_Mode', 'Item', 'Quantity', 'Rate', 'Amount', 'Subtotal', 'Discount', 'Shipping', 'Total']
            columns = ', '.join(x for x in columns_list)
            values = list(data_dict.values())
            if isinstance(values[0], int) or isinstance(values[0], float):
                val_st = str(values[0])
            elif values[0] == 'N/A' or isinstance(values[0], 'None'):
                val_st = None
            else:
                val_st = "'" + str(values[0]) + "'"
            
            for i in range(1, len(values)):
                if isinstance(values[i], int) or isinstance(values[i], float):
                    val_st = val_st + ", " + str(values[i])
                else:
                    val_st = val_st + ", " + "'" + str(values[i]) + "'"
        
            sql = "INSERT INTO %s ( %s )  VALUES ( %s );" % ('Invoices', columns, val_st)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            print("record added")
            df=df._append([data_dict], ignore_index=True)
        else:
            print("No match found.")
       
        print("********************DONE***************")
    cursor.close()
    df.head()
    return df