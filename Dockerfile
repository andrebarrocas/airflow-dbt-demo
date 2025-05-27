FROM apache/airflow:2.7.1

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install dbt and data science packages
RUN pip install --no-cache-dir \
    dbt-core==1.7.3 \
    dbt-postgres==1.7.3 \
    pandas==1.5.3 \
    numpy==1.24.3 \
    scipy==1.10.1 \
    psycopg2-binary==2.9.7

# Verify dbt installation
RUN dbt --version 