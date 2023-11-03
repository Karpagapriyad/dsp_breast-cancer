import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    layout="wide",
    page_title= "Breast Cancer Prediction",
    page_icon= "breast_cancer_logo.png"
)

st.sidebar.success("")


# Create a Streamlit app title
st.title("Prediction Page")
# st.image("breast_cancer_logo.jpg", use_column_width=True)

# Section for Single Sample Prediction
st.header("Single Sample Prediction")

# Create input widgets for single sample features
radius = st.number_input("Radius", min_value=0.0, step=0.01, value=50.0)
area = st.number_input("Area", min_value=0.0, step=0.01, value=50.0)
texture = st.number_input("Texture", min_value=0.0,  step=0.01, value=50.0)
perimeter = st.number_input("Perimeter", min_value=0.0, step=0.01, value=50.0)


# Create a button to trigger single sample prediction
if st.button("Predict Single Sample"):
    # Collect user input and prepare the data
    input_data = {
        "mean_radius ": radius,
        "mean_texture": area,
        "mean_perimeter": texture,
        "mean_area": perimeter
    }

    # Make a request to your model API to get the prediction
    api_url = "http://127.0.0.1:8000/predict"
    response = requests.post(api_url, json=input_data)
    if response.status_code == 200:
        prediction_response = response.json()
        prediction_value = prediction_response.get("prediction", "N/A")
        st.write("Prediction (Single):", prediction_value)
    else:
        st.write("Error:", response.status_code)


# Section for Batch Prediction
st.header("Batch Prediction")

# Create a file uploader widget for CSV files
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Create a button to trigger batch prediction
if csv_file is not None and st.button("Predict Batch"):
    # Read the uploaded CSV file
    batch_data = pd.read_csv(csv_file)
    
    # Make a request to your model API for batch predictions
    batch_prediction_response = requests.post("http://127.0.0.1:8000/bulk_predict", json=batch_data.to_dict(orient="records"))  # Replace with your API URL
    
    # Display the batch prediction results
    st.write("Batch Prediction Results:")
    st.write(batch_prediction_response.json())  # Assuming the API returns JSON

