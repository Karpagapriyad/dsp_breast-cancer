from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from starlette.responses import Response
from pydantic import BaseModel
import joblib
import pandas as pd
from io import StringIO
from typing import Optional
from Test_Connection import insert_json_data
from api_preprocesser import preprocessing
from typing import List
import json
import warnings

# Filter out the scikit-learn warning
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
app = FastAPI()

# Load the machine learning model
model = joblib.load('model_lri.joblib')


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
        print(prediction)
        return prediction
    if data.df_in is not None:
        df = pd.read_json(data.df_in, orient='records')
        prepocessed_df = preprocessing(df)
        predictions = model.predict(prepocessed_df)
        predictions_list = predictions.tolist()
        return {"predictions": predictions_list}
        


def make_prediction(features):
    # Convert features to a list for model prediction
    features_list = [features.mean_radius, features.mean_texture, features.mean_perimeter, features.mean_area]
    
    feature_json = '{"mean_radius" : "'+str(features.mean_radius)+'","mean_texture" : "'+str(features.mean_texture)+'","mean_perimeter" : "'+str(features.mean_perimeter)+'","mean_area" : "'+str(features.mean_area)+'"}'
    
    # Make predictions using the loaded model
    prediction = model.predict([features_list])[0]
    
    # Map prediction to 'benign' or 'malignant'
    prediction_label = 'benign' if prediction == 0 else 'malignant'

    # Append prediction to features
    features_json = json.loads(feature_json)
    features_json['diagnosis'] = prediction_label
    return features_json


# @app.get('/past_predictions', response_model=List[PastPrediction])
# def get_past_predictions():
#     cursor.execute("SELECT features, prediction FROM past_predictions")
#     past_predictions = []
#     for row in cursor.fetchall():
#         features_json = json.loads(row[0])
#         prediction_label = row[1]
#         past_predictions.append({"features": features_json, "prediction": prediction_label})

#     return past_predictions
