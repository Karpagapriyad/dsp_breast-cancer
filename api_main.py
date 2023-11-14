from fastapi import FastAPI, HTTPException, UploadFile
from starlette.responses import Response
from pydantic import BaseModel, ValidationError
import joblib
import pandas as pd
from io import StringIO
from db_connection import connect_to_database
from Test_Connection import insert_data_from_csv, insert_json_data
from api_preprocesser import preprocessing
from typing import List
import json
import warnings

# Filter out the scikit-learn warning
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
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


@app.post('/predict')
def predict(features: Features):
    # if isinstance(features, list):
    #     print("there")
    #     csv_text = features.read()
    #     df = pd.read_csv(StringIO(csv_text.decode('utf-8')))
    #     processed_df = preprocessing(df)
    #     predictions = [make_prediction(Features(**row)) for row in processed_df.to_dict('records')]
    #     csv_data = processed_df.copy()
    #     csv_data['prediction'] = predictions
    #     csv_string = csv_data.to_csv(index=False)
    #     insert_data_from_csv("breast_cancer", "prediction_table", csv_data=csv_string)
    #     print("yes")
    #     return csv_string
    # else:
    #     # Handle single prediction
    #     print("here")
    #     prediction = make_prediction(features)
    #     insert_json_data("breast_cancer", "prediction_table", json_data=prediction)
    #     print(prediction)
    #     return prediction
    print(features)
    # is_json = features.strip().startswith('{') and features.strip().endswith('}')
    # is_csv = '\n' in features and ',' in features
    # if isinstance(features, list):
    #     print("here")
    #     # csv_text = features.read()
    #     # df = pd.read_csv(StringIO(csv_text.decode('utf-8')))
    #     processed_df = preprocessing(features)
    #     predictions = [make_prediction(Features(**row)) for row in processed_df.to_dict('records')]
    #     csv_data = processed_df.copy()
    #     csv_data['prediction'] = predictions
    #     csv_string = csv_data.to_csv(index=False)
    #     insert_data_from_csv("breast_cancer", "prediction_table", csv_data=csv_string)
    #     print("yes")
    #     return csv_string
    # else:
    prediction = make_prediction(features)
    insert_json_data("breast_cancer", "prediction_table", json_data=prediction)
    print(prediction)
    return prediction


def make_prediction(features):
    # Convert features to a list for model prediction
    features_list = [features.mean_radius, features.mean_texture, features.mean_perimeter, features.mean_area]

    feature_json = '{"mean_radius" : "' + str(features.mean_radius) + '","mean_texture" : "' + str(
        features.mean_texture) + '","mean_perimeter" : "' + str(features.mean_perimeter) + '","mean_area" : "' + str(
        features.mean_area) + '"}'

    # Make predictions using the loaded model
    prediction = model.predict([features_list])[0]

    # Map prediction to 'benign' or 'malignant'
    prediction_label = 'benign' if prediction == 0 else 'malignant'

    # Append prediction to features
    features_json = json.loads(feature_json)
    features_json['diagnosis'] = prediction_label
    return features_json


@app.get('/past_predictions', response_model=List[PastPrediction])
def get_past_predictions():
    cursor.execute("SELECT features, prediction FROM past_predictions")
    past_predictions = []
    for row in cursor.fetchall():
        features_json = json.loads(row[0])
        prediction_label = row[1]
        past_predictions.append({"features": features_json, "prediction": prediction_label})

    return past_predictions
