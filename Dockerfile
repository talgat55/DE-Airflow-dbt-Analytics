FROM apache/airflow:2.10.5-python3.11

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir \
    "dbt-core==1.10.22" \
    "dbt-postgres==1.10.0" \
    pandas \
    faker \
    psycopg2-binary \
    python-dotenv