from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List

# Define default arguments
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['your-email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

def validate_data_quality(**context) -> Dict[str, List]:
    """
    Validate data quality using pandas
    Returns a dictionary with validation results
    """
    try:
        # Get connection from Airflow's connection management
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        
        df = pd.read_sql(
            """
            SELECT * FROM raw.orders 
            WHERE order_date >= CURRENT_DATE - INTERVAL '7 days'
            AND order_date <= CURRENT_DATE
            """,
            con=pg_hook.get_conn()
        )
        
        validation_results = {
            'errors': [],
            'warnings': []
        }

        # 1. Check for missing values
        missing_counts = df.isnull().sum()
        for column, count in missing_counts.items():
            if count > 0:
                validation_results['warnings'].append(
                    f"Column {column} has {count} missing values"
                )

        # 2. Check for data type consistency
        for column in df.select_dtypes(include=[np.number]).columns:
            invalid_numbers = df[~df[column].apply(lambda x: pd.to_numeric(x, errors='coerce')).notnull()].shape[0]
            if invalid_numbers > 0:
                validation_results['errors'].append(
                    f"Column {column} has {invalid_numbers} invalid numeric values"
                )

        # 3. Check for value ranges
        if 'amount' in df.columns:
            invalid_amounts = df[df['amount'] < 0].shape[0]
            if invalid_amounts > 0:
                validation_results['errors'].append(
                    f"Found {invalid_amounts} negative amounts"
                )

        # 4. Check for duplicates
        if 'order_id' in df.columns:
            duplicates = df[df.duplicated(['order_id'])].shape[0]
            if duplicates > 0:
                validation_results['errors'].append(
                    f"Found {duplicates} duplicate order IDs"
                )

        # 5. Check for date consistency
        if 'order_date' in df.columns:
            current_date = datetime.now().date()
            future_dates = df[df['order_date'] > current_date].shape[0]
            if future_dates > 0:
                validation_results['errors'].append(
                    f"Found {future_dates} orders with future dates"
                )

        # 6. Statistical validations
        if 'amount' in df.columns:
            avg_amount = df['amount'].mean()
            std_amount = df['amount'].std()
            outliers = df[abs(df['amount'] - avg_amount) > 3 * std_amount].shape[0]
            if outliers > 0:
                validation_results['warnings'].append(
                    f"Found {outliers} potential outliers in amount"
                )

        # Push validation results to XCom for downstream tasks
        context['task_instance'].xcom_push(
            key='validation_results',
            value=validation_results
        )

        # Fail the task if there are errors
        if validation_results['errors']:
            raise ValueError(f"Data validation failed: {validation_results['errors']}")

        return validation_results

    except Exception as e:
        context['task_instance'].xcom_push(
            key='validation_error',
            value=str(e)
        )
        raise

def generate_validation_report(**context):
    """Generate a report from validation results"""
    validation_results = context['task_instance'].xcom_pull(
        key='validation_results',
        task_ids='validate_data'
    )
    
    report = """
    Data Validation Report
    =====================
    
    Errors:
    -------
    {}
    
    Warnings:
    ---------
    {}
    """.format(
        '\n'.join(validation_results['errors']) if validation_results['errors'] else 'None',
        '\n'.join(validation_results['warnings']) if validation_results['warnings'] else 'None'
    )
    
    # Save report or send it somewhere
    context['task_instance'].xcom_push(key='validation_report', value=report)
    return report

# Create DAG
with DAG(
    'data_validation_pipeline',
    default_args=default_args,
    description='Data validation pipeline using pandas',
    schedule_interval='0 5 * * *',  # Run at 5 AM daily
    catchup=False
) as dag:

    # 1. Validate data using pandas
    validate_data = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data_quality
    )

    # 2. Generate validation report
    create_report = PythonOperator(
        task_id='create_validation_report',
        python_callable=generate_validation_report
    )

    # 3. Run dbt models if validation passes
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt_project && dbt run --profiles-dir .',
    )

    # Define task dependencies
    validate_data >> create_report >> dbt_run 