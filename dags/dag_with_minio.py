from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'debora',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_minio_v1',
    default_args=default_args,
    description='Using the bucket',
    start_date=datetime(2023, 12, 4),
    schedule_interval='0 3 * * *',
    catchup=False #if false it will run from the current day onwards, if true it will run since start_date
) as dag: 
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_conn_id',
        mode='poke', ## keep on checking the bucket using the poke_interval until timeout finishes
        poke_interval=5,
        timeout=30

    )

    task1

