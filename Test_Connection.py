from db_connection import connect_to_database, connect_to_postgres
import csv
import json
from psycopg2 import sql
from sqlalchemy import create_engine
import pandas as pd
from urllib.parse import quote_plus


def create_db(db_name):
    connection = connect_to_postgres()
    connection.autocommit = True
    cursor = connection.cursor() 
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    cursor.close()
    connection.close()


def create_table(db_name, table_name):
    connection = connect_to_database(db_name)
    cursor = connection.cursor()
    create_table_query = f'''CREATE TABLE {table_name}(id SERIAL PRIMARY KEY,"mean radius" FLOAT,"mean texture" FLOAT,"mean perimeter" FLOAT,"mean area" FLOAT,"diagnosis" VARCHAR(255));'''
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def insert_json_data(db_name, table_name, json_data):
    connection = connect_to_postgres()
    cursor = connection.cursor()
    db_check_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';"
    cursor.execute(db_check_query)
    existing_database = cursor.fetchone()

    if not existing_database:
        create_db(db_name)
    cursor.close()
    connection.close()
    
    connection = connect_to_database(db_name)
    cursor = connection.cursor()
    table_check_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]
    print(table_exists)
    if not table_exists:
        create_table(db_name, table_name)
    json_data = json.dumps(json_data)
    json_data = json.loads(json_data)  # Parse JSON string to dictionary
    radius_mean = json_data.get('mean_radius')
    texture_mean = json_data.get('mean_texture')
    perimeter_mean = json_data.get('mean_perimeter')
    area_mean = json_data.get('mean_area')
    diagnosis = json_data.get('diagnosis')

    insert_query = f'''
                INSERT INTO {table_name} ("mean radius", "mean texture", "mean perimeter", "mean area", diagnosis)
                VALUES ({radius_mean},{texture_mean},{perimeter_mean},{area_mean},'{diagnosis}')
            '''
    print(insert_query)
    cursor.execute(insert_query)
    connection.commit()
    print("Data inserted successfully!")
    if connection:
        cursor.close()
        connection.close()
        
def insert_csv_data(db_name, table_name, df_data):
    connection = connect_to_postgres()
    cursor = connection.cursor()
    db_check_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';"
    cursor.execute(db_check_query)
    existing_database = cursor.fetchone()

    if not existing_database:
        create_db(db_name)
    cursor.close()
    connection.close()
    
    connection = connect_to_database(db_name)
    cursor = connection.cursor()
    table_check_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]
    print(table_exists)
    if not table_exists:
        create_table(db_name, table_name)
    pd.DataFrame(df_data)
    my_password = "123456"
    encoded_password = quote_plus(my_password)
    engine = create_engine(f'postgresql://postgres:{encoded_password}@localhost/{db_name}')
    df_data.to_sql('prediction_table', con=engine, if_exists='append', index=False) 
    if connection:
        cursor.close()
        connection.close()
        
def past_prediction(db_name, table_name):
    connection = connect_to_postgres()
    cursor = connection.cursor()
    db_check_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';"
    cursor.execute(db_check_query)
    existing_database = cursor.fetchone()

    if not existing_database:
        create_db(db_name)
    cursor.close()
    connection.close()
    
    connection = connect_to_database(db_name)
    cursor = connection.cursor()
    table_check_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]
    if not table_exists:
        create_table(db_name, table_name)
    select_query = f'''select "mean radius", "mean texture", "mean perimeter", "mean area", "diagnosis" from {table_name}'''
    cursor.execute(select_query)
    predicted_data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    if connection:
        cursor.close()
        connection.close()
    return {"prediction_data": predicted_data, "columns" : columns}




