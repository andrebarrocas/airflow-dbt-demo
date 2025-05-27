from airflow.models import Connection
from airflow import settings
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
    try:
        # Check if connection already exists
        existing_conn = session.query(Connection).filter_by(conn_id=conn.conn_id).first()
        if existing_conn is not None:
            # Update existing connection
            existing_conn.host = conn.host
            existing_conn.login = conn.login
            existing_conn.password = conn.password
            existing_conn.schema = conn.schema
            existing_conn.port = conn.port
        else:
            # Add new connection
            session.add(conn)
        session.commit()
    except Exception as e:
        print(f"Error handling connection: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    create_conn() 