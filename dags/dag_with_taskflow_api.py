from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task

default_args = {
    'owner': 'debora',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

@dag(dag_id='dag_with_task_flow_api_v02',
     default_args=default_args,
     start_date=datetime(2023, 12, 3),
     schedule_interval='@daily')

def hello_world_etl():


    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Debora',
            'last_name': 'Santos'
        }
    
    @task()
    def get_age():
        return 30
    
    @task()
    def greet(first_name, last_name, age):
        print(f"Hello my name is {first_name} {last_name} and I'm {age} years old ")

    name_dict =  get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'],
        last_name=name_dict['last_name'],
         age=age)

greet_dag = hello_world_etl()
