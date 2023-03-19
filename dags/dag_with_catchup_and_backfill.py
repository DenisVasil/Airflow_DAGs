from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'Denis',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='dag_with_catchup_and_backfill_v02',
    default_args=default_args,
    description='This a DAG with catchup',
    start_date=datetime(2022, 7, 30, 2),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo This is a simple task!'
    )
    task1
