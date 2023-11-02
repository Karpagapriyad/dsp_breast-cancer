from fastapi import FastAPI, HTTPException, Query, Body
import psycopg2
from pydantic import BaseModel
from datetime import datetime

# Create a FastAPI instance
app = FastAPI()

# Database connection setup
database_url = "postgresql://postgres:password@localhost/dbname"
conn = psycopg2.connect(database_url)
cur = conn.cursor()

# Define a SQL query for creating the predictions table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    input_features TEXT,
    output_prediction TEXT,
    prediction_date TIMESTAMP,
    source TEXT
);
"""

# Execute the query and commit the changes
cur.execute(create_table_query)
conn.commit()

# Pydantic models for request and response
class PredictionRequest(BaseModel):
    input_features: str

class PredictionResponse(BaseModel):
    output_prediction: str

class PastPredictionResponse(BaseModel):
    id: int
    input_features: str
    output_prediction: str
    prediction_date: datetime
    source: str

# Endpoint for making predictions
@app.post("/predict/", response_model=PredictionResponse)
def predict(prediction_request: PredictionRequest, source: str = Query(...)):
    # Perform your model prediction here
    # For this example, we'll just return the input features
    input_features = prediction_request.input_features
    prediction_date = datetime.now()
    
    # Save the prediction to the database
    insert_query = """
    INSERT INTO predictions (input_features, output_prediction, prediction_date, source)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(insert_query, (input_features, "Your Model's Prediction", prediction_date, source))
    conn.commit()
    
    return {"output_prediction": "Your Model's Prediction"}

# Endpoint for getting past predictions
@app.get("/past-predictions/", response_model=list[PastPredictionResponse])
def past_predictions():
    select_query = """
    SELECT * FROM predictions;
    """
    cur.execute(select_query)
    db_predictions = cur.fetchall()
    
    past_predictions = []
    for db_prediction in db_predictions:
        past_predictions.append({
            "id": db_prediction[0],
            "input_features": db_prediction[1],
            "output_prediction": db_prediction[2],
            "prediction_date": db_prediction[3],
            "source": db_prediction[4]
        })
    
    return past_predictions
