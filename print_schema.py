import os
import pymssql

conn = pymssql.connect(
    server="datagenies.database.windows.net",
    user="sqladmin",
    password="@dmin123",
    database="InvoicesDB",
    as_dict=True
)  

def generate_prompt(question):
    SQL_QUERY = "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"

    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)

    create_queries = []
    tables_list = []

    records = cursor.fetchall()
    for row in records:
        create_query = f"CREATE TABLE [{row['TABLE_SCHEMA']}].[{row['TABLE_NAME']}] ("
        table_row = [f"[{row['TABLE_SCHEMA']}].[{row['TABLE_NAME']}]"]

        COLUMNS_QUERY = f"select COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{row['TABLE_NAME']}'"
        cursor.execute(COLUMNS_QUERY)
        columns = cursor.fetchall()
        first_col = True
        table_columns = []
        for column in columns:
            table_columns.append(column['COLUMN_NAME'])
            if first_col:
                create_query += f"{column['COLUMN_NAME']} {column['DATA_TYPE']}"
                if column["CHARACTER_MAXIMUM_LENGTH"]:
                    create_query += f"({column['CHARACTER_MAXIMUM_LENGTH']})"
                first_col = False
            else:
                create_query += f", {column['COLUMN_NAME']} {column['DATA_TYPE']}"
                if column['CHARACTER_MAXIMUM_LENGTH']:
                    create_query += f"({column['CHARACTER_MAXIMUM_LENGTH']})"
        table_row.append(table_columns)

        CONSTRAINTS_QUERY = f"SELECT cu.COLUMN_NAME, con.CONSTRAINT_TYPE FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE cu INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS con ON cu.CONSTRAINT_NAME = con.CONSTRAINT_NAME WHERE cu.TABLE_NAME='{row['TABLE_NAME']}';"
        cursor.execute(CONSTRAINTS_QUERY)
        constraints = cursor.fetchall()
        table_constraints = []
        for constraint in constraints:
            table_constraints.append((constraint['CONSTRAINT_TYPE'], constraint['COLUMN_NAME']))
            create_query += f", {constraint['CONSTRAINT_TYPE']}({constraint['COLUMN_NAME']})"
        table_row.append(table_constraints)
        create_query += ");"

        create_queries.append(create_query)
        tables_list.append(table_row)

    joins = []
    for index in range(len(tables_list)):
        if tables_list[index][2]:
            for constraint in tables_list[index][2]:
                if 'PRIMARY KEY' in constraint:
                    for s_index in range(len(tables_list)):
                        if s_index == index:
                            continue
                        if constraint[1] in tables_list[s_index][1]:
                            joins.append(f"-- {tables_list[s_index][0]}.{constraint[1]} can be joined with {tables_list[index][0]}.{constraint[1]}")

    templateFile = open("Resources/prompt_template_sql.txt", "r")

    prompt_template = templateFile.read()
    
    new_prompt = prompt_template.format(question, "\n".join(create_queries[0:]), "\n".join(joins[0:]), question)
    
    return new_prompt

question = "Give me OrderDetails along with Product details for orders with total more than 2000"

print(generate_prompt(question))