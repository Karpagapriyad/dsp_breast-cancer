import streamlit as st
import pandas as pd
import requests
import json

st.header("Past Prediction")

past_prediction_data = requests.get("http://127.0.0.1:8000/past_predictions")

past_prediction = past_prediction_data.text

data_dict = json.loads(past_prediction)

df = pd.DataFrame(data_dict["prediction_data"], columns = data_dict["columns"])

st.table(df)