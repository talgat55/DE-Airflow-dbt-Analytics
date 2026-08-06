from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project"
DBT_DIR = f"{PROJECT_DIR}/ecommerce_analytics"
DBT_PROFILES_DIR = f"{PROJECT_DIR}/config"

default_args = {
    "owner": "tg",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="ecommerce_dbt_pipeline",
    description="Generate source data load raw tables and run dbt",
    default_args=default_args,
    start_date=datetime(2026, 8, 1),
    schedule=None,
    catchup=False,
    tags=["dbt", "airflow", "postgres", "ecommerce"],
) as dag:
    generate_data = BashOperator(
        task_id="generate_data",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "python scripts/generate_data.py"
        ),
    )

    load_raw = BashOperator(
        task_id="load_raw",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "python scripts/load_raw.py"
        ),
    )

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=(
            f"cd {DBT_DIR} && "
            f"dbt debug --profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd {DBT_DIR} && "
            f"dbt build --profiles-dir {DBT_PROFILES_DIR}"
        ),
    )

    generate_data >> load_raw >> dbt_debug >> dbt_build