from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta
import os
import requests
import pandas as pd


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
    def ingest_data():

        return
    return