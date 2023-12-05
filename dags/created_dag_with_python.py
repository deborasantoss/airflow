from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'debora',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')

    print(f"Hello World! My name is {first_name} {last_name} and my age {age}")

def get_name(ti):
    ti.xcom_push(key='first_name', value='Debora')
    ti.xcom_push(key='last_name', value='Santos')

def get_age(ti):
    ti.xcom_push(key='age', value=15)


with DAG(
    default_args=default_args,
    dag_id='dag_with_python_v5',
    description='First dag with python',
    start_date=datetime(2023, 12, 3),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        # op_kwargs={'age': 30}
    )
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name,
    )
    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age,
    )

    [task2, task3] >> task1