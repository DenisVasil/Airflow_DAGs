from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'Denis',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
# crontab guru
with DAG(
    dag_id='dag_with_crone_expression_v05',
    default_args=default_args,
    description='This is a DAG with crone expression',
    start_date=datetime(2022, 12, 27),
    schedule_interval='0 3 * * Tue-Fri'
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo dag with crone expression'
    )
    task1
