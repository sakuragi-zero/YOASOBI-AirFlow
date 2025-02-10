from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

from butler_task import greet, next_talk, hawaii, tea_party, end_day

with DAG(
    dag_id='one_day',
    schedule_interval=None,
    start_date=datetime(2025, 2, 1),
    catchup=False
) as dag:
    
    greet_task = PythonOperator(
        task_id='greet_task',
        python_callable=greet
    )
    
    branch_task = BranchPythonOperator(
        task_id='branch_task',
        python_callable=next_talk
    )
    
    hawaii_task = PythonOperator(
        task_id='hawaii_task',
        python_callable=hawaii
    )
    
    tea_party_task = PythonOperator(
        task_id='tea_party_task',
        python_callable=tea_party
    )
    
    end_task = PythonOperator(
        task_id='end_task',
        python_callable=end_day
    )
    
    trigger_vacation_hawaii = TriggerDagRunOperator(
        task_id='trigger_vacation_hawaii',
        trigger_dag_id='vacation_hawaii'
    )
    
    greet_task >> branch_task
    branch_task >> [hawaii_task, tea_party_task, end_task]
    hawaii_task >> trigger_vacation_hawaii
