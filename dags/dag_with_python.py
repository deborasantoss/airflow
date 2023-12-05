from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'debora',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def get_sklearn():
    import sklearn
    print(f"sklean version {sklearn.__version__}")

def get_matplotlib():
    import matplotlib
    print(f"matplotlib version {matplotlib.__version__}")

with DAG(
    dag_id='dag_with_python_v12',
    default_args=default_args,
    description='Python tgest',
    start_date=datetime(2023, 11, 29, 2),
    schedule_interval='@daily',
    catchup=False 

) as dag: 
    
    get_sklearn = PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn

    )

    get_matplotlib = PythonOperator(
        task_id='get_matplotlib',
        python_callable=get_matplotlib

    )

    get_sklearn >> get_matplotlib