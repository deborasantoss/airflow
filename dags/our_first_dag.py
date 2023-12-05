from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'debora',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='our_first_dag_v3',
    default_args=default_args,
    description='This is our first dag that we write',
    start_date=datetime(2023, 11, 29, 2),
    schedule_interval='@daily'

) as dag: 
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is my first!"
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo hello world, this is my seconds after task 1!"
    )

    task3 = BashOperator(
        task_id='third_task',
        bash_command="echo Im task 3"
    )

    ##one way
    task1.set_downstream(task2)
    task1.set_downstream(task3)

    #second
    