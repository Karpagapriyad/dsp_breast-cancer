from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import psycopg2

app = FastAPI()

# Load the machine learning model
model = joblib.load('model_lri.joblib')

# Set up PostgreSQL connection
conn = psycopg2.connect(database="your_db", user="postgres", password="Jerry@126", host="localhost", port="5432")
cursor = conn.cursor()

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
    return predict([features])

@app.post('/bulk_predict', response_model=PredictionResponse)
def predict_bulk(features_list: List[Features]):
    return predict(features_list)

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

    # Save features and prediction to PostgreSQL
    cursor.execute("INSERT INTO past_predictions (mean_radius, mean_texture, mean_perimeter, mean_area, prediction) VALUES (%s, %s, %s, %s, %s)", (features.mean_radius, features.mean_texture, features.mean_perimeter, features.mean_area, prediction_label))
    conn.commit()

    return prediction_label

@app.get('/past_predictions', response_model=List[PastPrediction])
def get_past_predictions():
    cursor.execute("SELECT mean_radius, mean_texture, mean_perimeter, mean_area, prediction FROM past_predictions")
    past_predictions = []
    for row in cursor.fetchall():
        features = Features(mean_radius=row[0], mean_texture=row[1], mean_perimeter=row[2], mean_area=row[3])
        prediction_label = row[4]
        past_predictions.append({"features": features, "prediction": prediction_label})

    return past_predictions
