from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

app = Flask("http://localhost:8501/")

# Replace with your database connection details
DATABASE_URI = 'postgresql://username:password@localhost/your_database_name'