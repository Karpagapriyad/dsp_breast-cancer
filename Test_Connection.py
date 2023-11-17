from db_connection import connect_to_database, connect_to_postgres
import csv
import json
from psycopg2 import sql


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
    create_table_query = f"CREATE TABLE {table_name}(id SERIAL PRIMARY KEY,radius_mean FLOAT,texture_mean FLOAT,perimeter_mean FLOAT,area_mean FLOAT,diagnosis VARCHAR(255));"
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()


# def insert_data_from_csv(db_name,table_name, file):
#     cursor = connection.cursor()
#     db_check_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';"
#     cursor.execute(db_check_query)
#     existing_database = cursor.fetchone()[0]

#     if not existing_database:
#         create_db(connection)
    
    


#     table_check_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
#     cursor.execute(table_check_query)
#     table_exists = cursor.fetchone()[0]

#     if not table_exists:
#         create_table(connection)

#     with open(file, 'r') as csv_file:
#         csv_reader = csv.reader(csv_file)
#         next(csv_reader)
#     for row in csv_reader:
#         id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis = row
#         insert_query = f'''
#             INSERT INTO table_name (id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis)
#             VALUES ({id}, {radius_mean}, {texture_mean}, {perimeter_mean}, {area_mean}, '{diagnosis}')
#             '''
#         cursor.execute(insert_query)

#     connection.commit()
#     cursor.close()


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
                INSERT INTO {table_name} (radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis)
                VALUES ({radius_mean},{texture_mean},{perimeter_mean},{area_mean},'{diagnosis}')
            '''
    cursor.execute(insert_query)
    connection.commit()
    print("Data inserted successfully!")
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
    select_query = f'''select id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis from {table_name}'''
    cursor.execute(select_query)
    predicted_data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    if connection:
        cursor.close()
        connection.close()
    return {"prediction_data": predicted_data, "columns" : columns}


# def create_not_quality_data_table(connection):
#     cursor = connection.cursor()

#     create_table_query = '''
#                 CREATE TABLE IF NOT EXISTS not_quality_data (
#                     id SERIAL PRIMARY KEY,
#                     file_name VARCHAR(255),
#                     negative_value_count INTEGER,
#                     missing_value_count INTEGER
#                 )
#             '''

#     cursor.execute(create_table_query)
#     connection.commit()


# def insert_not_quality_data(file_name, negative_value_count, missing_value_count):
#     cursor = connection.cursor()
#     insert_query = f'''
#                 INSERT INTO not_quality_data (file_name, negative_value_count, missing_value_count)
#                 VALUES ('{file_name}', {negative_value_count}, {missing_value_count})
#             '''
#     cursor.execute(insert_query)
#     connection.commit()
#     if connection:
#         cursor.close()
#         connection.close()


# connection = connect_to_database()


