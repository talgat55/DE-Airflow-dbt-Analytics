import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"

FILE_CONFIG = {
    "customers.csv": "raw.customers",
    "products.csv": "raw.products",
    "orders.csv": "raw.orders",
    "order_items.csv": "raw.order_items",
    "payments.csv": "raw.payments",
}

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=os.getenv("POSTGRES_PORT", "5436"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

def load_csv(
    filename: str,
    table_name: str,
) -> int:
    csv_path = RAW_DATA_DIR / filename

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}"
        )

    dataframe = pd.read_csv(csv_path)

    if dataframe.empty:
        print(f"{filename}: empty file")
        return 0

    columns = list(dataframe.columns)

    rows = [
        tuple(
            None if pd.isna(value) else value
            for value in row
        )
        for row in dataframe.itertuples(
            index=False,
            name=None,
        )
    ]

    sql = f"""
        INSERT INTO {table_name} (
            {", ".join(columns)}
        )
        VALUES %s
        ON CONFLICT DO NOTHING;
    """

    connection = get_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                execute_values(
                    cursor,
                    sql,
                    rows,
                    page_size=1000,
                )

        print(
            f"{filename} -> {table_name}: "
            f"{len(rows)} rows processed"
        )

        return len(rows)

    finally:
        connection.close()


def load_all() -> None:
    total = 0

    for filename, table_name in FILE_CONFIG.items():
        total += load_csv(
            filename=filename,
            table_name=table_name,
        )

    print(f"Total processed rows: {total}")

if __name__ == "__main__":
    load_all()