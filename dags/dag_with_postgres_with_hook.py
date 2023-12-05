
from airflow import DAG
import csv
import logging
from tempfile import NamedTemporaryFile
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args = {
    'owner': 'debora',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def postgres_to_s3(execution_date):
    hook =PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    print("connected to postgres")
    cursor.execute("select * from orders where date <= '2022-05-01'")
    with NamedTemporaryFile(mode='w', suffix=f"{execution_date}") as f: #create in memory
    # with open(f"dags/get_orders_{execution_date}.txt", "w") as f: create locally
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerow(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info(f"Saved get_orders_{execution_date}")
        s3_hook = S3Hook(aws_conn_id="minio_conn_id")
        s3_hook.load_file(
            filename=f.name,
            key=f"orders/{execution_date}.txt",
            bucket_name="airflow",
            replace=True
    )
    logging.info("Orders files have been pushed to s3", f.name)


with DAG(
    dag_id='dag_with_hook_v4',
    default_args=default_args,
    description='Using the bucket and postgres',
    start_date=datetime(2023, 12, 4),
    schedule_interval='0 3 * * *',
    catchup=False #if false it will run from the current day onwards, if true it will run since start_date
) as dag: 
    task1 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=postgres_to_s3

    )

    task1
