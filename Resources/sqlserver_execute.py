import os
import pymssql
import pandas as pd

conn = pymssql.connect(
    server=os.environ["SERVER_ADDRESS"],
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE_NAME"],
    as_dict=True
)  

def execute_query(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)

    except Exception as e:
        print(e)
        return e
    
    query_results = cursor.fetchall()

    # Create a Pandas DataFrame
    data_frame = pd.DataFrame(query_results)
    return data_frame