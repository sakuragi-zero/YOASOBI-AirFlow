- Airflowの設定ファイルairflow.cfg
```bash
[core]
load_examples = False
```

- Airflowの初期設定  
airflow.cfgを生成しデフォルトのSQLiteデータベースが作成される  
```bash
export AIRFLOW_HOME=$(pwd)/airflow
poetry run airflow db init
```
- ログイン用のユーザーを作成
```bash
poetry run airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```
- UI起動コマンド  
```bash
poetry run airflow scheduler & poetry run airflow webserver --port 8080
```