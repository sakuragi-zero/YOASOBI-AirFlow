from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from functions.get_env import test, test1


class LoadTask:
    """環境変数を扱うタスクを定義するクラス"""

    def __init__(self, env="xxxx-yyyy"):
        self.env = env

    def test(self):
        """env を用いた処理"""
        return test(self.env)

    def test1(self):
        """test1 を実行し、結果を返す"""
        return test1(self.env)

    @classmethod
    def load_task(cls, **kwargs):
        """
        Airflow の PythonOperator 用メソッド
        op_kwargs から `env` を取得し、クラスのインスタンスを生成して処理を実行する。
        """
        env = kwargs.get("env", "xxxx-yyyy")  # デフォルト値を指定
        instance = cls(env)  # クラスのインスタンスを作成
        return instance.test1()  # test1() を実行


# DAG の定義
with DAG(
    dag_id="example_env_passing",
    schedule_interval=None,
    start_date=datetime(2025, 2, 1),
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="run_test1",
        python_callable=LoadTask.load_task,  # クラスメソッドを渡す
        op_kwargs={"env": "こんにちは"},  # `env` を Airflow から渡す
    )


