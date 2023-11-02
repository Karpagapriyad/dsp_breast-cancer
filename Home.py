import streamlit as st
import psycopg2
from psycopg2 import sql

st.set_page_config(
    layout="wide",
    page_title= "Breast Cancer Prediction",
    page_icon= "breast_cancer_logo.png"
)

st.sidebar.success("")

with st.container():
    logo_col, title_col = st.columns([1, 3])
    # with logo_col:
    #     st.image("breast_cancer_logo.png", width=100)
    with title_col:
        st.title("Breast Cancer Prediction")


def main():
    
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="Jerry@126",
            host="localhost",
            port="5432"
        )
        connection.set_isolation_level(0) 
        cursor = connection.cursor()

        # Check if the database already exists
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(sql.Literal("breast_cancer")))

        database_exists = cursor.fetchone()

        if not database_exists:
            # Create the database if it doesn't exist
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("breast_cancer")))

        connection.close()

        # Connect to the newly created database
        new_connection = psycopg2.connect(
            user="postgres",
            password="Jerry@126",
            host="localhost",
            port="5432",
            dbname="breast_cancer"
        )

        return new_connection

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
