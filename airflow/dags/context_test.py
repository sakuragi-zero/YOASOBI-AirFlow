from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from functions.get_env import test, test1


class LoadTask:
    def __init__(self):
        self.env = "xxxx-yyyy"
    
    def test(self):
        return test(self.env)
    
    def test1(self, env=None):  
        """env を受け取れるように修正"""
        return test1(env if env else self.env)

    @staticmethod
    def load_task(env="デフォルト値", **kwargs):
        """AirflowのPythonOperatorで実行するためのメソッド"""
        instance = LoadTask()  # クラスのインスタンスを作成
        return instance.test1(env)  # `env` を渡して `test1` を実行


# DAG の定義
with DAG(
    dag_id="example_env_passing",
    schedule_interval=None,
    start_date=datetime(2025, 2, 1),
    catchup=False,
) as dag:
    
    task = PythonOperator(
        task_id="run_test1",
        python_callable=LoadTask.load_task,  # クラス内の static メソッドを渡す
        op_kwargs={"env": "こんにちは"},  # `env` を渡す
    )

