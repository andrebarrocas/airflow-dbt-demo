from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'simple_dbt_pipeline',
    default_args=default_args,
    description='A simple dbt pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    # Debug command to check environment
    debug_env = BashOperator(
        task_id='debug_env',
        bash_command='pwd && ls -la && which dbt && dbt --version',
        dag=dag
    )

    # Run dbt with debug output
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt_project && dbt debug --profiles-dir . && dbt run --profiles-dir . --debug',
        dag=dag
    )

    # Test dbt models
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt_project && dbt test --profiles-dir . --debug',
        dag=dag
    )

    debug_env >> dbt_run >> dbt_test 