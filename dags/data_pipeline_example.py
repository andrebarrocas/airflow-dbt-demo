from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['your-email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# Example Python function
def validate_data(**context):
    """Check if data meets quality standards"""
    # Your validation logic here
    print("Validating data...")
    return True

def transform_data(**context):
    """Transform the data"""
    # Your transformation logic here
    print("Transforming data...")
    return True

# Create DAG
with DAG(
    'complete_data_pipeline',
    default_args=default_args,
    description='A complete data pipeline example',
    schedule_interval='0 5 * * *',  # Run at 5 AM daily
    catchup=False
) as dag:

    # 1. Wait for upstream data
    wait_for_upstream = ExternalTaskSensor(
        task_id='wait_for_upstream',
        external_dag_id='upstream_dag',
        external_task_id='final_task',
        timeout=3600,
        mode='reschedule'
    )

    # 2. Data validation
    validate = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data
    )

    # 3. Run dbt models
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt_project && dbt run --profiles-dir .',
    )

    # 4. Run dbt tests
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt_project && dbt test --profiles-dir .',
    )

    # 5. Transform data
    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    # 6. Send notification
    notify = EmailOperator(
        task_id='send_notification',
        to='team@example.com',
        subject='Data Pipeline Complete',
        html_content='The data pipeline has completed successfully.'
    )

    # Define task dependencies
    wait_for_upstream >> validate >> dbt_run >> dbt_test >> transform >> notify 