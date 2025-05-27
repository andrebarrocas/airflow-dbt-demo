# Simple dbt Airflow Project

A minimal example showing how to run dbt models using Apache Airflow.

## Prerequisites

- Docker
- Docker Compose
- Python 3.8 or later
- pip (Python package installer)

## Setup

1. Create and activate a Python virtual environment:
```bash
# Create virtual environment
python3.9 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. Build the custom Airflow image:
```bash
docker build -t custom-airflow-dbt .
```

3. Start the services:
```bash
docker compose up -d
```

4. Access Airflow web interface:
- URL: http://localhost:8080
- Username: airflow
- Password: airflow

## Project Structure

```
.
├── dags/                   # Airflow DAGs
│   └── dbt_dag.py         # Simple dbt pipeline
├── dbt_project/           # dbt project files
│   ├── models/            # dbt models
│   │   └── example/       # Example models
│   │       └── orders.sql # Simple orders model
│   ├── profiles.yml       # dbt connection profiles
│   └── dbt_project.yml    # dbt project configuration
├── setup/                 # Setup scripts
│   └── init_connections.py # Airflow connection initialization
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Custom Airflow image with dbt
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Testing the Pipeline

1. The DAG will automatically run daily, but you can test it manually:
   - Go to the Airflow UI
   - Find the 'simple_dbt_pipeline' DAG
   - Click the "Play" button to trigger it manually

2. The pipeline has two tasks:
   - dbt_run: Creates the orders table
   - dbt_test: Runs dbt tests

3. To verify the results:
   - Connect to the PostgreSQL database:
     ```bash
     docker exec -it simple-dbt-airflow-project-postgres-1 psql -U airflow -d airflow
     ```
   - Query the orders table:
     ```sql
     SELECT * FROM public.orders;
     ```

## Troubleshooting

If you encounter any issues:

1. Check the Airflow task logs in the UI
2. Verify the containers are running:
   ```bash
   docker-compose ps
   ```
3. Check container logs:
   ```bash
   docker-compose logs -f
   ```
4. Common issues:
   - If you see permission errors, make sure you're running commands with appropriate privileges
   - If containers fail to start, try stopping and removing all containers:
     ```bash
     docker-compose down -v
     docker-compose up -d
     ```
   - If dbt fails to connect, check the profiles.yml configuration and make sure PostgreSQL is running 