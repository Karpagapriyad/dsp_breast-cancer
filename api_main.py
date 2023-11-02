from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import psycopg2

app = FastAPI()

# Load the machine learning model
model = joblib.load('model_lri.joblib')

# Set up PostgreSQL connection
conn = psycopg2.connect(database="your_db", user="your_user", password="your_password", host="your_host", port="your_port")
cursor = conn.cursor()

class Features(BaseModel):
    mean_radius: float
    mean_texture: float
    mean_perimeter: float
    mean_area: float

class PredictionResponse(BaseModel):
    prediction: str

class PastPredictionResponse(BaseModel):
    past_predictions: list

@app.post('/predict', response_model=PredictionResponse)
def predict(features: Features):
    # Convert features to a list for model prediction
    features_list = [features.mean_radius, features.mean_texture, features.mean_perimeter, features.mean_area]
    
    # Make predictions using the loaded model
    prediction = model.predict([features_list])[0]
    
    # Map prediction to 'benign' or 'malignant'
    prediction_label = 'benign' if prediction == 0 else 'malignant'

    # Save prediction and features to PostgreSQL
    cursor.execute("INSERT INTO predictions (mean_radius, mean_texture, mean_perimeter, mean_area, prediction) VALUES (%s, %s, %s, %s, %s)", (features.mean_radius, features.mean_texture, features.mean_perimeter, features.mean_area, prediction_label))
    conn.commit()

    return {"prediction": prediction_label}

@app.get('/past_predictions', response_model=PastPredictionResponse)
def past_predictions():
    # Retrieve past predictions and features from the database
    cursor.execute("SELECT mean_radius, mean_texture, mean_perimeter, mean_area, prediction FROM predictions")
    past_predictions = []
    for row in cursor.fetchall():
        features = {
            'mean_radius': row[0],
            'mean_texture': row[1],
            'mean_perimeter': row[2],
            'mean_area': row[3]
        }
        prediction_label = row[4]
        past_predictions.append({'features': features, 'prediction': prediction_label})

    return {"past_predictions": past_predictions}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
