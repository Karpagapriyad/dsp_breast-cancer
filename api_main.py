from fastapi import FastAPI, File, HTTPException, UploadFile, Response
from pydantic import BaseModel
import joblib
import pandas as pd
from io import StringIO
from db_connection import connect_to_database
from Test_Connection import insert_data_from_csv, insert_json_data
from api_preprocesser import preprocessing
from typing import List
import json


app = FastAPI()

# Load the machine learning model
model = joblib.load('model_lri.joblib')

# Set up PostgreSQL connection
connection = connect_to_database()
cursor = connection.cursor()


class Features(BaseModel):
    mean_radius: float
    mean_texture: float
    mean_perimeter: float
    mean_area: float


class PredictionResponse(BaseModel):
    prediction: str


class PastPrediction(BaseModel):
    features: Features
    prediction: str


@app.post('/predict', response_model=PredictionResponse)
def predict_single(features: Features):
    prediction = make_prediction(features)
    return {"prediction": prediction}


@app.post('/bulk_predict', response_model=Response)
async def predict_bulk(file: UploadFile):
    try:
        csv_text = await file.read()
        df = pd.read_csv(StringIO(csv_text.decode('utf-8')))
        
        # Preprocess the CSV data using the provided Preprocessing function
        processed_df = preprocessing(df)
        
        # Make predictions using the loaded model
        predictions = [make_prediction(Features(**row)) for row in processed_df.to_dict('records')]
        
        # Create a CSV string with predictions appended to features
        csv_data = processed_df.copy()
        csv_data['prediction'] = predictions
        csv_string = csv_data.to_csv(index=False)
        
        return Response(content=csv_string, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=predictions.csv"})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error processing the bulk data")


def predict(features):
    if isinstance(features, list):
        # Handle bulk prediction
        predictions = []
        for feature in features:
            prediction = make_prediction(feature)
            predictions.append(prediction)
        return {"prediction": predictions}
    else:
        # Handle single prediction
        prediction = make_prediction(features)
        return {"prediction": prediction}


def make_prediction(features):
    # Convert features to a list for model prediction
    features_list = [features.mean_radius, features.mean_texture, features.mean_perimeter, features.mean_area]
    
    # Make predictions using the loaded model
    prediction = model.predict([features_list])[0]
    
    # Map prediction to 'benign' or 'malignant'
    prediction_label = 'benign' if prediction == 0 else 'malignant'

    # Append prediction to features
    features_json = features.json()
    features_json["prediction"] = prediction_label

    # Save features and prediction to the database
    insert_json_data(json_data=features_json)  # Function to insert JSON data
    insert_data_from_csv(csv_data=features_json)  # Function to insert CSV data

    return prediction_label


@app.get('/past_predictions', response_model=List[PastPrediction])
def get_past_predictions():
    cursor.execute("SELECT features, prediction FROM past_predictions")
    past_predictions = []
    for row in cursor.fetchall():
        features_json = json.loads(row[0])
        prediction_label = row[1]
        past_predictions.append({"features": features_json, "prediction": prediction_label})

    return past_predictions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)