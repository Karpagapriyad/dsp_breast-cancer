import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    layout="wide",
    page_title= "Breast Cancer Prediction",
    page_icon= "breast_cancer_logo.png"
)

st.sidebar.success("")

# #Header section
# with st.container():
#     logo_col, title_col = st.columns([1, 3])
#     with logo_col:
#         st.image("breast_cancer_logo.png", width=100)
#     with title_col:
#         st.title("Breast Cancer Prediction")

# Create a Streamlit app title
st.title("Prediction Page")
# st.image("breast_cancer_logo.jpg", use_column_width=True)

# Section for Single Sample Prediction
st.header("Single Sample Prediction")

# Create input widgets for single sample features
radius = st.number_input("Radius", min_value=0.0, max_value=100.0, step=0.01, value=50.0)
area = st.number_input("Area", min_value=0.0, max_value=100.0, step=0.01, value=50.0)
texture = st.number_input("Texture", min_value=0.0, max_value=100.0, step=0.01, value=50.0)
perimeter = st.number_input("Perimeter", min_value=0.0, max_value=100.0, step=0.01, value=50.0)
# feature5 = st.number_input("Feature 5", min_value=0.0, max_value=100.0, step=0.01, value=50.0)
# feature6 = st.number_input("Feature 6", min_value=0.0, max_value=100.0, step=0.01, value=50.0)
# feature2 = st.slider("Feature 2", min_value=0, max_value=100, value=50)
# feature3 = st.text_input("Feature 3", "Default Value")
# feature4 = st.selectbox("Feature 4", ["Option 1", "Option 2", "Option 3"])
# feature5 = st.checkbox("Feature 5")

# Create a button to trigger single sample prediction
if st.button("Predict Single Sample"):
    # Collect user input and prepare the data
    input_data = {
        "feature1": radius,
        "feature2": area,
        "feature3": texture,
        "feature4": perimeter
    }
    
    # Make a request to your model API to get the prediction
    prediction_response = requests.post("your_model_api_url", json=input_data)  # Replace with your API URL
    
    # Display the prediction result
    st.write("Single Sample Prediction Result:")
    st.write(prediction_response.json())  # Assuming the API returns JSON

# Section for Batch Prediction
st.header("Batch Prediction")

# Create a file uploader widget for CSV files
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Create a button to trigger batch prediction
if csv_file is not None and st.button("Predict Batch"):
    # Read the uploaded CSV file
    batch_data = pd.read_csv(csv_file)
    
    # Make a request to your model API for batch predictions
    batch_prediction_response = requests.post("your_model_api_url_batch", json=batch_data.to_dict(orient="records"))  # Replace with your API URL
    
    # Display the batch prediction results
    st.write("Batch Prediction Results:")
    st.write(batch_prediction_response.json())  # Assuming the API returns JSON


