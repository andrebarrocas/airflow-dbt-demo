# Simple dbt Airflow Project

This project demonstrates how to run dbt models using Apache Airflow for orchestration.

## Project Structure

```
.
├── dags/                   # Airflow DAGs
├── dbt_project/           # dbt project files
│   ├── models/            # dbt models
│   ├── profiles.yml       # dbt connection profiles
│   └── dbt_project.yml    # dbt project configuration
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Custom Airflow image with dbt
└── README.md             # This file
```

## Getting Started

1. Build the custom Airflow image:
   ```bash
   docker build -t custom-airflow-dbt .
   ```

2. Update the docker-compose.yml to use your custom image:
   - Change the image from `apache/airflow:2.7.1` to `custom-airflow-dbt` for both airflow services

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Access Airflow web interface:
   - Open http://localhost:8080 in your browser
   - Default credentials:
     - Username: airflow
     - Password: airflow

5. The DAG will run automatically once per day, or you can trigger it manually from the Airflow UI.

## Components

- **Airflow DAG**: Located in `dags/dbt_dag.py`, runs dbt models daily
- **dbt Models**: Located in `dbt_project/models/`, contains your data transformations
- **PostgreSQL**: Used as both Airflow metadata database and target database for dbt models

## Notes

- The project uses PostgreSQL as the target database for simplicity
- The dbt models are very simple examples and should be modified for your use case
- All services run in Docker containers for easy setup and portability 