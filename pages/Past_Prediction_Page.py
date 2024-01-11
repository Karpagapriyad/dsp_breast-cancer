import streamlit as st
import pandas as pd
import requests
import json

st.header("Past Prediction")

# for selection from dropdown list
source = st.selectbox("Select source of predictions", ("webapp", "scheduled predictions", "all"))


# for selecting a date range
start_date = st.date_input("Select start date")
end_date = st.date_input("Select end date")

# If both start date and end date are selected
if start_date and end_date:

    # Convert to strings in the format YYYY-MM-DD
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    


    # Fetch past prediction data
    past_prediction_data = requests.get("http://127.0.0.1:8000/past_predictions")
    past_prediction = past_prediction_data.text
    data_dict = json.loads(past_prediction)
    

    # Convert prediction data to DataFrame
    df = pd.DataFrame(data_dict["prediction_data"], columns=data_dict["columns"])
    

    # Convert the 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    

    # Filter DataFrame based on the selected date range
    filtered_df = df[(df['timestamp'] >= start_date_str) & (df['timestamp'] <= end_date_str)]
    

    # Display the filtered table
    st.table(filtered_df)