from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from functions.get_env import test, test1

class LoadTask:
    def __init__(self):
        self.env = "xxxx-yyyy"
    
    def test(self):
        return test(self.env)
    
    def test1(self, env=None):  # env を受け取れるように変更
        return test1(env if env else self.env)

load = LoadTask()

def load_task(**context):  # `env` を受け取れるように修正
    env = context.get("env", "デフォルト値")  # Airflow から `env` を取得
    return load.test1(env)

with DAG(
    dag_id="example_env_passing",
    schedule_interval=None,
    start_date=datetime(2025, 2, 1),
    catchup=False,
) as dag:
    
    task = PythonOperator(
        task_id="run_test1",
        python_callable=load_task,  # メソッドの参照ではなく関数にする
        op_kwargs={"env": "こんにちは"},  # `env` を渡す
    )
