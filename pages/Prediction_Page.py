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

# Section for Single Sample Prediction
st.header("Single Sample Prediction")

# Create input widgets for single sample features
radius = st.number_input("Radius", min_value=0.0, step=0.01, value=50.0)
area = st.number_input("Area", min_value=0.0, step=0.01, value=50.0)
texture = st.number_input("Texture", min_value=0.0, step=0.01, value=50.0)
perimeter = st.number_input("Perimeter", min_value=0.0, step=0.01, value=50.0)

# Create a button to trigger single sample prediction
if st.button("Predict Single Sample"):
    input_data = {
        "mean_radius": float(radius),
        "mean_area": float(area),
        "mean_texture": float(texture),
        "mean_perimeter": float(perimeter)
    }
    payload ={
        "features" : input_data,
        "df_in" : None
    }
    prediction_response = requests.post("http://127.0.0.1:8000/predict", json=payload) 
    st.write("Prediction (Single):", prediction_response.text)

# Section for Batch Prediction
st.header("Batch Prediction")

# Create a file uploader widget for CSV files
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Create a button to trigger batch prediction
if csv_file is not None and st.button("Predict Batch"):
    # Read the uploaded CSV file
    df = pd.read_csv(csv_file)
    df_json = df.to_json(orient='records')
    payload ={
        "features" : None,
        "df_in" : df_json
    }
    batch_prediction_response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    
    st.write("Batch Prediction Results:")
    st.write(batch_prediction_response.text)

