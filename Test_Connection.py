from db_connection import connect_to_database
import csv
import json


def create_db(connection, db_name):
    cursor = connection.cursor()
    create_db_query = f"CREATE DATABASE {db_name};"
    cursor.execute(create_db_query)
    cursor.close()


def create_table(connection, table_name):
    cursor = connection.cursor()
    create_table_query = f"CREATE TABLE {table_name}(id SERIAL PRIMARY KEY,radius_mean FLOAT,texture_mean FLOAT,perimeter_mean FLOAT,area_mean FLOAT,diagnosis VARCHAR(255));"
    cursor.execute(create_table_query)
    cursor.close()


def insert_data_from_csv(db_name,table_name, file):
    cursor = connection.cursor()
    db_check_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';"
    cursor.execute(db_check_query)
    existing_database = cursor.fetchone()[0]

    if not existing_database:
        create_db(connection)


    table_check_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        create_table(connection)

    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
    for row in csv_reader:
        id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis = row
        insert_query = f'''
            INSERT INTO table_name (id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis)
            VALUES ({id}, {radius_mean}, {texture_mean}, {perimeter_mean}, {area_mean}, '{diagnosis}')
            '''
        cursor.execute(insert_query)

    connection.commit()
    cursor.close()


def insert_json_data(db_name, table_name, json_data):
    cursor = connection.cursor()
    db_check_query = f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';"
    cursor.execute(db_check_query)
    existing_database = cursor.fetchone()[0]

    if not existing_database:
        create_db(connection, db_name)
    table_check_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]
    if not table_exists:
        create_table(connection,table_name)
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


def create_not_quality_data_table(connection):
    cursor = connection.cursor()

    create_table_query = '''
                CREATE TABLE IF NOT EXISTS not_quality_data (
                    id SERIAL PRIMARY KEY,
                    file_name VARCHAR(255),
                    negative_value_count INTEGER,
                    missing_value_count INTEGER
                )
            '''

    cursor.execute(create_table_query)
    connection.commit()


def insert_not_quality_data(file_name, negative_value_count, missing_value_count):
    cursor = connection.cursor()
    insert_query = f'''
                INSERT INTO not_quality_data (file_name, negative_value_count, missing_value_count)
                VALUES ('{file_name}', {negative_value_count}, {missing_value_count})
            '''
    cursor.execute(insert_query)
    connection.commit()
    if connection:
        cursor.close()
        connection.close()


connection = connect_to_database()


