from fastapi import FastAPI
from pydantic import BaseModel  # Import any other libraries you need

app = FastAPI()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## Replace 'your_postgres_url' with your actual PostgreSQL connection URL
database_url = "postgresql://username:password@localhost/dbname"

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

## Define your table's structure
#class Prediction(Base):
  #  __tablename__ = "predictions"
#
 #   id = Column(Integer, primary_key=True, index=True)
  #  input_features = Column(String, index=True)
   # output_prediction = Column(String)
    #timestamp = Column(DateTime)

    # Add more columns if needed

    # Add any relationships between tables if needed


@app.get("/")
async def root():
    return {"message": "Hello World"}

