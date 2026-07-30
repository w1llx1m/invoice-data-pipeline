from sqlalchemy import create_engine
import pandas as pd
import os

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DEBUG = os.getenv("DEBUG_MODE") == "True"


def get_engine():
    try:
        engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow")
        # testando a conexão antes de avançar
        with engine.connect() as conn:
            pass
        return engine
    except Exception as e:
        print(f"[LOAD PIPELINE] Could not connect to Postgres at 'postgres:5432/{DB_NAME}'. "
          f"Check if the container is up and credentials are correct. Details: {e}")
        raise

def load_data(df: pd.DataFrame, engine, table_name: str):
    try:
        df.to_sql(table_name, engine, if_exists="append", index=False, method="multi")
        print(f"Bulk insert successful! {len(df)} rows loaded into '{table_name}'.")
    except Exception as e:
        print(f"[LOAD PIPELINE] Could not load data to Postgres at 'postgres:5432/{DB_NAME}'. "
                  f"Check if the container is up. Details: {e}")
        raise  # relança o erro para o Airflow marcar a task como falha