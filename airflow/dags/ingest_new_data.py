from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta
import os
import pandas as pd
# from data_ingestion_rough import save_validate_data


@dag (
    dag_id='Ingestion_job',
    description='check the new data to folder A for every 1 min',
    tags=['dsp', 'Ingestion'],
    schedule=timedelta(minutes=1),
    start_date=days_ago(n=0, hour=1),
    catchup=False
)

def ingestion_job():
    @task
    def ingest_data(folder_path="Folder-A"):
        dfs = None
        all_files = os.listdir(folder_path)
        for file_name in all_files:
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            dfs = df if dfs is None else pd.concat([dfs, df], ignore_index=True)

        if dfs is None or dfs.empty:
         raise ValueError("No data found in the specified folder.")
        return dfs
    @task
    def validate_great_expectation(dfs):
       
       return 

    ingest_data = ingest_data()
    validation = validate_great_expectation(ingest_data)

    ingest_data >> validation

prediction_dag = ingestion_job()
    