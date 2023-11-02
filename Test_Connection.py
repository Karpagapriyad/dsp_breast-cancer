import psycopg2
import csv
import json
 
# Function to establish a database connection
def connect_to_database(dbname, username, password, host, port):
    conn = psycopg2.connect(
        dbname=dbname,
        user=username,
        password=password,
        host=host,
        port=port
    )
    return conn
 
# Function to check if a database exists
def database_exists(dbname, username, password, host, port):
    try:
        conn = connect_to_database('postgres', username, password, host, port)
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s;",
            (dbname,)
        )
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()
 
# Function to create a new database if it doesn't exist
def create_database_if_not_exists(dbname, username, password, host, port):
    if not database_exists(dbname, username, password, host, port):
        try:
            conn = connect_to_database('postgres', username, password, host, port)
            cur = conn.cursor()
            cur.execute(
                "CREATE DATABASE %s;",
                (dbname,)
            )
            print(f"Database '{dbname}' created successfully")
        finally:
            cur.close()
            conn.close()
 
# Function to check if a table exists
def table_exists(table_name, conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);",
        (table_name,)
    )
    return cur.fetchone()[0]
 
# Function to create a new table if it doesn't exist
def create_table_if_not_exists(table_name, header_columns, conn):
    if not table_exists(table_name, conn):
        try:
            cur = conn.cursor()
            columns = ', '.join([f"{col} TEXT" for col in header_columns])
            create_table_query = f'''
            CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                {columns}
            );
            '''
            cur.execute(create_table_query)
            print(f"Table '{table_name}' created successfully")
        finally:
            cur.close()
 
# Function to insert data from CSV file into the table
def insert_csv_data_into_table(csv_filename, table_name, dbname, username, password, host, port):
    conn = connect_to_database(dbname, username, password, host, port)
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        header_columns = csv_reader.fieldnames
        create_table_if_not_exists(table_name, header_columns, conn)
        try:
            cur = conn.cursor()
            for row in csv_reader:
                columns = ', '.join(row.keys())
                values = ', '.join(['%s'] * len(row))
                insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({values});'
                cur.execute(insert_query, list(row.values()))
            conn.commit()
            print(f"Data from CSV file '{csv_filename}' inserted into '{table_name}' table successfully")
        finally:
            cur.close()
            conn.close()
 
# Function to insert a single data point from JSON file into the table
def insert_json_data_into_table(json_filename, table_name, dbname, username, password, host, port):
    conn = connect_to_database(dbname, username, password, host, port)
    with open(json_filename, 'r') as jsonfile:
        data = json.load(jsonfile)
        create_table_if_not_exists(table_name, data.keys(), conn)
        try:
            cur = conn.cursor()
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({values});'
            cur.execute(insert_query, list(data.values()))
            conn.commit()
            print(f"Data from JSON file '{json_filename}' inserted into '{table_name}' table successfully")
        finally:
            cur.close()
            conn.close()
 
# Example usage
if __name__ == "__main__":
    dbname = "Breast Cancer Prediction Database"
    username = "postgres"
    password = "Bholenath!2023"
    host = "localhost"
    port = "5432"
    csv_filename = "your_csv_file.csv"
    json_filename = "your_json_file.json"
    csv_table_name = "csv_table"
    json_table_name = "json_table"
 
    create_database_if_not_exists(dbname, username, password, host, port)
    insert_csv_data_into_table(csv_filename, csv_table_name, dbname, username, password, host, port)
    insert_json_data_into_table(json_filename, json_table_name, dbname, username, password, host, port)