import os
from airflow import DAG
from airflow.utils.dates import datetime
from airflow.decorators import task
from airflow.operators.postgres import PostgresOperator
from scripts.python.download_file import download_pageviews, fetch_page

datasource_url = "https://dumps.wikimedia.org/other/pageviews/2024/2024-10/pageviews-20241001-000000.gz"
downloads_folder = os.path.expanduser("~/projects/cde/airflow/airflowcde/dags/core_sentiment/pageviews")
output_sql_file = '/opt/airflow/dags/core_sentiment/scripts/sql/insert_data.sql'

with DAG(
    dag_id="pageview",
    start_date=datetime(2024, 10, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    # PostgreSQL Operator to create the table
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='your_postgres_conn_id',  # Replace with your connection ID
        sql=open('/opt/airflow/dags/sql/create_table.sql', 'r').read(),
    )

    @task
    def download_pageviews_task():
        return download_pageviews(datasource_url, downloads_folder)

    @task
    def fetch_page_task(csv_file):
        fetch_page(csv_file, output_sql_file)

    # Push to database
    push_to_postgres = PostgresOperator(
        task_id="push_to_postgres",
        postgres_conn_id='postgre_default',
        sql=open(output_sql_file, 'r').read(),  
        autocommit=True 
    )

    # Notify
    notify = PostgresOperator(
        task_id="notify",
        postgres_conn_id='postgre_default', 
        sql="SELECT 'Data processing complete and pushed to PostgreSQL.' AS message;"
    )

    csv_file = download_pageviews_task()
    fetch_page_task(csv_file) >> create_table >> push_to_postgres >> notify