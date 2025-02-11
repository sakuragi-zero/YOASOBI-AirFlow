# LoadTask の変遷と最適化

これまでのコードの変遷と最適化の過程を時系列順にまとめました。

---

## 変遷と最適化の要点

| バージョン | 変更点・課題 | 改善ポイント |
|------------|------------|-------------|
| **① 初期版** | `LoadTask` クラスを作成し、インスタンス変数 `env` を利用して処理 | `test1()` 内で `test()` を呼び出す際に `self` を考慮 |
| **② Airflow 版** | `LoadTask` を `PythonOperator` で実行する形に修正 | `PythonOperator` に渡すため `load_task` を `staticmethod` で定義 |
| **③ `classmethod` 最適化版** | `@staticmethod` の問題（クラスの動的なインスタンス生成不可）を修正 | `@classmethod` を使い `cls(env)` で適切にインスタンス化 |

---

## ① 初期版: クラス設計

```python
class LoadTask:
    def __init__(self):
        self.env = "xxxx-yyyy"

    def test(self):
        print(self.env)
        return self.env + "-1999"

    def test1(self):
        x = self.test()  # メソッドの呼び出しミスを修正
        y = "01-01"
        return x + y  # 文字列の結合

課題
test1() の x = self.test がメソッドを呼び出していない (() が必要)
クラスの外部から test1() を呼び出せるが、Airflow でタスク実行する仕組みがない

② Airflow 版: PythonOperator 対応

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from functions.get_env import test, test1

class LoadTask:
    def __init__(self):
        self.env = "xxxx-yyyy"
    
    def test(self):
        return test(self.env)
    
    def test1(self):
        return test1(self.env)

    @staticmethod
    def load_task(env="デフォルト値"):
        """Airflow の PythonOperator で使用するための静的メソッド"""
        instance = LoadTask(env)
        return instance.test1()

with DAG(
    dag_id="example_env_passing",
    schedule_interval="@daily",
    start_date=datetime(2025, 2, 1),
    catchup=False,
) as dag:
    
    task = PythonOperator(
        task_id="run_test1",
        python_callable=LoadTask.load_task,  # クラスメソッドを渡す
        op_kwargs={"env": "こんにちは"},  # `env` を渡す
    )


改善点
PythonOperator で LoadTask.load_task を python_callable として渡せる
@staticmethod でクラス外部から直接実行できるように修正
課題
@staticmethod では サブクラスを作成した場合 LoadTask 固定になり、拡張性が低い
LoadTask(env) を 手動でインスタンス化 しないといけない（冗長）

③ @classmethod 最適化版: 継承対応 & 拡張性アップ

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from functions.get_env import test, test1


class LoadTask:
    """環境変数を扱うタスクを定義するクラス"""

    def __init__(self, env="xxxx-yyyy"):
        self.env = env

    def test(self):
        return test(self.env)

    def test1(self):
        return test1(self.env)

    @classmethod
    def load_task(cls, **kwargs):
        """
        Airflow の PythonOperator 用メソッド
        op_kwargs から `env` を取得し、クラスのインスタンスを生成して処理を実行する。
        """
        env = kwargs.get("env", "xxxx-yyyy")  # デフォルト値を設定
        instance = cls(env)  # ✅ cls を利用し、動的にインスタンスを作成
        return instance.test1()


# DAG の定義
with DAG(
    dag_id="example_env_passing",
    schedule_interval="@daily",
    start_date=datetime(2025, 2, 1),
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="run_test1",
        python_callable=LoadTask.load_task,  # クラスメソッドを渡す
        op_kwargs={"env": "こんにちは"},  # `env` を動的に渡す
    )

最適化ポイント
@classmethod を使用し、cls(env) で 適切にインスタンスを作成
LoadTask を継承した場合も cls(env) で動的にインスタンス生成が可能
op_kwargs から 環境変数 env を取得し適切に処理


バージョン	変更点・最適化
① 初期版	基本的なクラス構造 (test1 の呼び出し修正)
② Airflow 版	PythonOperator に対応 (@staticmethod を利用)
③ 最適化版	@classmethod に変更し、動的なクラス生成 & 継承対応

結論: @classmethod を採用した最適版
継承しやすく、拡張性が高い
cls(env) により、インスタンス管理が簡潔
Airflow の PythonOperator に最適

