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
def create_table(connection, table_name, table_schema):
    cursor = connection.cursor()

    cursor.execute(f"CREATE TABLE {table_name} ({table_schema});")
    print(f"Table '{table_name}' created successfully.")

    cursor.close()
    connection.commit()


# Function to insert data from CSV file into the table
def insert_data_from_csv(file_path):
    cursor = connection.cursor()
    table_check_query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'your_table_name')"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        create_table(connection, table_name, table_schema)

        # Read data from the CSV file and insert it into the table.
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if it exists in the CSV file.
    for row in csv_reader:
        id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis = row
        insert_query = f'''
            INSERT INTO your_table_name (id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis)
            VALUES ({id}, {radius_mean}, {texture_mean}, {perimeter_mean}, {area_mean}, '{diagnosis}')
            '''
        cursor.execute(insert_query)

    connection.commit()
    cursor.close()


# Function to insert a single data point from JSON file into the table
def insert_json_data_into_table(json_filename, table_name, dbname, username, password, host, port):
    cursor = connection.cursor()
    table_check_query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'your_table_name')"
    cursor.execute(table_check_query)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        create_table(connection, table_name, table_schema)
    json_data = json.loads(json_data)  # Parse JSON string to dictionary
    id = json_data.get("id")
    radius_mean = json_data.get("radius_mean")
    texture_mean = json_data.get("texture_mean")
    perimeter_mean = json_data.get("perimeter_mean")
    area_mean = json_data.get("area_mean")
    diagnosis = json_data.get("diagnosis")

    insert_query = f'''
                INSERT INTO your_table_name (id, radius_mean, texture_mean, perimeter_mean, area_mean, diagnosis)
                VALUES ({id}, {radius_mean}, {texture_mean}, {perimeter_mean}, {area_mean}, '{diagnosis}')
            '''
    cursor.execute(insert_query)
    connection.commit()
    print("Data inserted successfully!")
    if connection:
        cursor.close()
        connection.close()

# Example usage
if __name__ == "__main__":
    db_name = "breast_cancer"
    user_name = "postgres"
    db_password = "123456"
    db_host = "localhost"
    port_no = "5432"
    table_name = 'past_prediction'
    table_schema = 'id SERIAL PRIMARY KEY, radius_mean FLOAT, texture_mean FLOAT, perimeter_mean FLOAT, area_mean FLOAT,diagnosis VARCHAR(255)'

    connection = connect_to_database(db_name, user_name, db_password, db_host, port_no)
    create_database_if_not_exists(connection, db_name)
    create_table(connection, table_name, table_schema)

