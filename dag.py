from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from scrapped_daily import *

def my_func():
    return new_data()
with DAG("dag", start_date=datetime(2022,1,31), 
    schedule_interval="@daily", catchup=False) as dag:
        A = PythonOperator(
            task_id="A",
            python_callable = my_func
        )

'''def task_done(ti):
    ti.xcom.pull(task_id="A")'''