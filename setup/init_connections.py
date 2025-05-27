from airflow.models import Connection
from airflow import settings
from airflow.models.crypto import get_fernet
from airflow.utils.session import create_session

def create_conn():
    conn = Connection(
        conn_id="postgres_default",
        conn_type="postgres",
        host="postgres",
        login="airflow",
        password="airflow",
        schema="airflow",
        port=5432
    )
    session = settings.Session()
    session.add(conn)
    session.commit()
    session.close()

if __name__ == "__main__":
    create_conn() 