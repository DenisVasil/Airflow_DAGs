import csv
import logging
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args = {
    'owner': 'Denis',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


def postgres_to_s3(ds_nodash, next_ds_nodash):
    # query data from PG and save it as a txt file
    hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute('''SELECT FROM orders
    WHERE date >=%s AND date <=%s ''',
                   (ds_nodash, next_ds_nodash))

    with NamedTemporaryFile(mode='w', suffix=f"{ds_nodash}") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info("Saved orders data in text file: %s",
                     f"dags/get_orders_{ds_nodash}.txt")
        # upload to s3  bucket
        s3_hook = S3Hook(aws_conn_id="minio_conn")
        s3_hook.load_file(
            filename=f.name,
            key=f"orders/{ds_nodash}.txt",
            bucket_name="airflow",
            replace=True
        )
        logging.info("Orders file %s has been pushed to S3!", f.name)

    # with open('dags/get_orders_{ds_nodash}.txt', 'w') as f:
    #     csv_writer = csv.writer(f)
    #     csv.writer.writerow([i[0] for i in cursor.description])
    #     csv.writer.writerows(cursor)
    # cursor.close()
    # conn.close()
    # logging.info('Saved orders data in txt file: %s',
    #              f'dags/get_orders_{ds_nodash}.txt')
    # s3_hook = S3Hook(aws_conn_id='minio_conn')
    # s3_hook.load_file(
    #     filename=f'dags/get_orders_{ds_nodash}.txt',
    #     key=f"orders/{ds_nodash}.txt",
    #     bucket_name="airflow",
    #     replace=True
    # )


with DAG(
    dag_id='dag_with_pg_hook_v04',
    default_args=default_args,
    description='Dag with Postgres hook',
    start_date=datetime(2022, 12, 29),
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id='postgres_to_s3',
        python_callable=postgres_to_s3
    )
    task1
