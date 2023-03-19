from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Denis',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


def get_sklearn():
    import sklearn
    print(f'scikit_learn version: {sklearn.__version__}')


def get_matplotlib():
    import matplotlib
    print(f'Matplotlib version: {matplotlib.__version__}')


with DAG(
    dag_id='dag_with_python_dependecies_v02',
    default_args=default_args,
    description='This DAG includes python packages',
    start_date=datetime(2022, 12, 25),
    schedule_interval='@daily',

) as dag:
    task1 = PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn,
    )
    task2 = PythonOperator(
        task_id='get_matplotlib',
        python_callable=get_matplotlib,
    )
task1 >> task2
