from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'debora',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_postgres_v03',
    default_args=default_args,
    description='This is our first dag that we write',
    start_date=datetime(2023, 12, 4),
    schedule_interval='0 0 * * *',
    catchup=False
) as dag: 
    task1 = PostgresOperator(
        task_id='create_post_',
        postgres_conn_id='postgres_localhost',
        sql="""
        
            create table if not exists dag_runs(
            dt date, 
            dag_id character varying,
            primary key (dt, dag_id)
            )

        """

    )
    task2 = PostgresOperator(
        task_id='insert_post_',
        postgres_conn_id='postgres_localhost',
        sql="""
            insert into dag_runs (dt, dag_id) values ('{{ds}}', '{{dag.dag_id}}')

        """

    )

    task1  >> task2