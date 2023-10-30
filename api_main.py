from fastapi import FastAPI, HTTPException, Query, Body
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime

# Create a FastAPI instance
app = FastAPI()

# Database connection setup
database_url = "postgresql://username:password@localhost/dbname"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a SQLAlchemy model for predictions
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    input_features = Column(String)
    output_prediction = Column(String)
    prediction_date = Column(DateTime)
    source = Column(String)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Pydantic models for request and response
class PredictionRequest(BaseModel):
    input_features: str

class PredictionResponse(BaseModel):
    output_prediction: str

class PastPredictionResponse(BaseModel):
    id: int
    input_features: str
    output_prediction: str
    prediction_date: DateTime
    source: str

# Endpoint for making predictions
@app.post("/predict/", response_model=PredictionResponse)
def predict(prediction_request: PredictionRequest, source: str = Query(...)):
    # Perform your model prediction here
    # For this example, we'll just return the input features
    input_features = prediction_request.input_features
    prediction_date = datetime.now()
    
    # Save the prediction to the database
    with SessionLocal() as db_session:
        db_prediction = Prediction(
            input_features=input_features,
            output_prediction="Your Model's Prediction",
            prediction_date=prediction_date,
            source=source
        )
        db_session.add(db_prediction)
        db_session.commit()
    
    return {"output_prediction": "Your Model's Prediction"}

# Endpoint for getting past predictions
@app.get("/past-predictions/", response_model=list[PastPredictionResponse])
def past_predictions():
    with SessionLocal() as db_session:
        db_predictions = db_session.query(Prediction).all()
    
    past_predictions = []
    for db_prediction in db_predictions:
        past_predictions.append({
            "id": db_prediction.id,
            "input_features": db_prediction.input_features,
            "output_prediction": db_prediction.output_prediction,
            "prediction_date": db_prediction.prediction_date,
            "source": db_prediction.source
        })
    
    return past_predictions
