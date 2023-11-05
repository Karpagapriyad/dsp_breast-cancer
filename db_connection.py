import psycopg2


def connect_to_database():
    connection = psycopg2.connect(
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
    return connection

