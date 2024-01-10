from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta
import os
import requests
import pandas as pd


@dag (
    dag_id='Prediction_job',
    description='check the new files from folder c and make prediction',
    tags=['dsp', 'prediction'],
    schedule=timedelta(minutes=5),
    start_date=days_ago(n=0, hour=1),
    catchup=False
)
def prediction_job():
    @task
    def check_new_data(folder_path ="Folder-C",time_threshold_minutes=5) -> pd.DataFrame:
        current_time = datetime.now()
        dfs = None
        all_files = os.listdir(folder_path)
        for file_name in all_files:
          file_path = os.path.join(folder_path, file_name)
          modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
          if (current_time - modification_time) < timedelta(minutes=time_threshold_minutes):
              df = pd.read_csv(file_path)
              dfs = df if dfs is None else pd.concat([dfs, df], ignore_index=True)
        return dfs if dfs is not None else pd.DataFrame()
    
    @task
    def make_prediction(df: pd.DataFrame):
        df_json = df.to_json(orient='records')
        payload = {
            "features": None,
            "df_in": df_json
        } 
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        return response.json()
    check_data = check_new_data()
    prediction = make_prediction(check_data)

    check_data >> prediction

prediction_dag = prediction_job()
    