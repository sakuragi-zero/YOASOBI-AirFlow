from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from butler_task import private_beach

with DAG(
    dag_id='vacation_hawaii',
    schedule_interval=None,
    start_date=datetime(2025, 2, 1),
    catchup=False
) as dag:
    vacation_hawaii = PythonOperator(
        task_id='private_beach_task',
        python_callable=private_beach
    )
