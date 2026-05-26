FROM apache/airflow:2.9.1-python3.10

# 1. Temporarily use root to install native Linux system packages
USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Switch back to the standard application user context to run pip safely
USER airflow

RUN pip install --no-cache-dir dbt-postgres==1.7.4

# 3. Switch back to root so your docker-compose "user: '0:0'" mapping remains fully functional
USER root