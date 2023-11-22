from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from starlette.responses import Response
from pydantic import BaseModel
import joblib
import pandas as pd
from io import StringIO
from typing import Optional
from Test_Connection import insert_json_data, insert_csv_data, past_prediction
from api_preprocesser import preprocessing
from typing import List
import json
import warnings

# Filter out the scikit-learn warning
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
app = FastAPI()

# Load the machine learning model
model = joblib.load('model_lrib.joblib')


class Features(BaseModel):
    mean_radius: float
    mean_texture: float
    mean_perimeter: float
    mean_area: float
    
class PredictionRequest(BaseModel):
    features: Optional[Features]
    df_in: Optional[str]

class PredictionResponse(BaseModel):
    prediction: str


class PastPrediction(BaseModel):
    features: Features
    prediction: str


@app.post('/predict')
def predict(data : PredictionRequest):
    if data.features is not None:
        prediction = make_prediction(data.features)
        insert_json_data("breast_cancer", "prediction_table", json_data=prediction)
        return prediction['diagnosis']
    if data.df_in is not None:
        df = pd.read_json(data.df_in, orient='records')
        prepocessed_df = preprocessing(df)
        scaled = core_scale(prepocessed_df)
        predictions = model.predict(scaled)
        predictions_list = predictions.tolist()

        # Map 0 to "benign" and 1 to "malignant"
        predictions_mapped = ['benign' if pred == 0 else 'malignant' for pred in predictions_list]

        prepocessed_df['diagnosis'] = predictions_mapped
        insert_csv_data("breast_cancer", "prediction_table", prepocessed_df)
        
        return {"predictions": predictions_mapped}
        
# This function is created tp scale the input csv
def core_scale(df):
    scaler = joblib.load('scaler_lri.joblib')
    scaled  = scaler.transform(df)
    return scaled


def make_prediction(features):
    # Convert features to a list for model prediction
    features_list = [features.mean_radius, features.mean_texture, features.mean_perimeter, features.mean_area]
    
    feature_json = '{"mean_radius" : "'+str(features.mean_radius)+'","mean_texture" : "'+str(features.mean_texture)+'","mean_perimeter" : "'+str(features.mean_perimeter)+'","mean_area" : "'+str(features.mean_area)+'"}'
    
    scalers = joblib.load('scaler_lri.joblib')

    scale_input = scalers.transform([features_list])

    prediction = model.predict(scale_input)[0]
    
    prediction_label = 'benign' if prediction == 0 else 'malignant'
    
    features_json = json.loads(feature_json)
    features_json['diagnosis'] = prediction_label
    return features_json


@app.get('/past_predictions')
def get_past_predictions():
    past_prediction_data = past_prediction("breast_cancer", "prediction_table")
    return past_prediction_data
   