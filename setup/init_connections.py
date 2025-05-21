from airflow import settings
from airflow.models import Connection
from airflow.utils.session import create_session

def init_connections():
    with create_session() as session:
        # Add PostgreSQL connection
        postgres_conn = Connection(
            conn_id='postgres_default',
            conn_type='postgres',
            host='postgres',
            schema='public',
            login='airflow',
            password='airflow',
            port=5432,
            extra={"database": "airflow"}  # Add database name explicitly
        )
        
        # Check if connection already exists
        if not session.query(Connection).filter(Connection.conn_id == postgres_conn.conn_id).first():
            session.add(postgres_conn)
            session.commit()

if __name__ == '__main__':
    init_connections() 