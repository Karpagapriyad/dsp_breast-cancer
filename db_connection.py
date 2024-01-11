import psycopg2


def connect_to_postgres():
    connection = psycopg2.connect(
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
    return connection

def connect_to_database(database_name):
    connection = psycopg2.connect(
        user="postgres",
        password="123456",
        host="localhost",
        port="5432",
        database = database_name
    )
    return connection

