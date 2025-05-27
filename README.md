# Simple dbt Airflow Project

A minimal example showing how to run dbt models using Apache Airflow.

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
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Custom Airflow image with dbt
└── README.md             # This file
```

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Build the custom Airflow image:
```bash
docker build -t custom-airflow-dbt .
```

2. Start the services:
```bash
docker-compose up -d
```

3. Access Airflow web interface:
- URL: http://localhost:8080
- Username: airflow
- Password: airflow

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