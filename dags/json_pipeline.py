"""DAG 2: JSON Transformation Pipeline"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {"owner": "findata_team", "start_date": datetime(2024, 1, 1)}

def transform_to_json():
    print("Transforming to JSON format...")

def load_json_to_snowflake():
    print("Loading JSON to VARIANT column...")

with DAG("json_transformation_pipeline", default_args=default_args, schedule_interval="@quarterly") as dag:
    transform = PythonOperator(task_id="transform", python_callable=transform_to_json)
    load = PythonOperator(task_id="load", python_callable=load_json_to_snowflake)
    transform >> load

