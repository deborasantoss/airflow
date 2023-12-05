from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'debora',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_catchup_v0q',
    default_args=default_args,
    description='This is our first dag that we write',
    start_date=datetime(2023, 12, 1),
    schedule_interval='@daily',
    catchup=True #if false it will run from the current day onwards, if true it will run since start_date
) as dag: 
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is my first!"
    )

    task1