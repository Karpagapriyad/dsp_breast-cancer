from db_connection import connect_to_database
import csv
import json


# Function to check if a database exists
def create_database_if_not_exists(connection, new_database_name):
    try:
        cursor = connection.cursor()

        # Check if the database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (new_database_name,))
        existing_database = cursor.fetchone()

        if not existing_database:
            # Create a new database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {new_database_name};")
            print(f"Database '{new_database_name}' created successfully.")
        else:
            print(f"Database '{new_database_name}' already exists.")

        # Close the cursor and commit the changes
        cursor.close()
        connection.commit()

    except Exception as error:
        print(f"Error: Unable to create database - {error}")


# Function to check if a table exists
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = '''
                CREATE TABLE IF NOT EXISTS prediction_table (
                    id SERIAL PRIMARY KEY,
                    radius_mean FLOAT,
                    texture_mean FLOAT,
                    perimeter_mean FLOAT,
                    area_mean FLOAT,
                    diagnosis VARCHAR(255)
                )
            '''
    cursor.execute(create_table_query)
    cursor.close()


# Function to insert data from CSV file into the table
def insert_data_from_csv(file, connection):
    cursor = connection.cursor()
    table_check_query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'prediction_table')"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        create_table(connection)

        # Read data from the CSV file and insert it into the table.
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if it exists in the CSV file.
    for row in csv_reader:
        id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis = row
        insert_query = f'''
            INSERT INTO prediction_table (id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis)
            VALUES ({id}, {radius_mean}, {texture_mean}, {perimeter_mean}, {area_mean}, '{diagnosis}')
            '''
        cursor.execute(insert_query)

    connection.commit()
    cursor.close()


# Function to insert a single data point from JSON file into the table
def insert_json_data( json_data, connection):
    cursor = connection.cursor()
    table_check_query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'prediction_table')"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        create_table(connection)
    json_data = json.loads(json_data)  # Parse JSON string to dictionary
    id = json_data.get("id")
    radius_mean = json_data.get("radius_mean")
    texture_mean = json_data.get("texture_mean")
    perimeter_mean = json_data.get("perimeter_mean")
    area_mean = json_data.get("area_mean")
    diagnosis = json_data.get("diagnosis")

    insert_query = f'''
                INSERT INTO prediction_table (id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis)
                VALUES ({id},{radius_mean},{texture_mean},{perimeter_mean},{area_mean},'{diagnosis}')
            '''
    cursor.execute(insert_query)
    connection.commit()
    print("Data inserted successfully!")
    if connection:
        cursor.close()
        connection.close()


def create_not_quality_data_table(connection):
    cursor = connection.cursor()

    # Define the SQL query to create the not quality data table.
    create_table_query = '''
                CREATE TABLE IF NOT EXISTS not_quality_data (
                    id SERIAL PRIMARY KEY,
                    file_name VARCHAR(255),
                    negative_value_count INTEGER,
                    missing_value_count INTEGER
                )
            '''

    # Execute the SQL query to create the table.
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


# Example usage

connection = connect_to_database()


