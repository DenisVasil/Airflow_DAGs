from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Denis',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


# def greet(age, ti):
#     name = ti.xcom_pull(task_ids='get_name')
#     print(f'Hello World! My name is {name} and I am {age} years old.')

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')

    print(
        f'Hello World! My name is {first_name} {last_name} and I am {age} years old.')


# def get_name():
#     return 'Denis'

def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='White')


def get_age(ti):
    ti.xcom_push(key='age', value=19)


with DAG(
    default_args=default_args,
    dag_id='dag_with_python_operator_v06',
    description='DAG using python operator',
    start_date=datetime(2022, 12, 27),
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        #op_kwargs={'age': 20}
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
