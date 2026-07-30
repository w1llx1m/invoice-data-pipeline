from sqlalchemy import create_engine, text
from pathlib import Path

def create_tables():
    try:
        engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")

        schema_path = Path(__file__).resolve().parent / "schema.sql"
        sql_script = schema_path.read_text()

        with engine.begin() as conn:
            conn.execute(text(sql_script))

        print("Tables created successfully.")
    except Exception as e:
        print(f"[CRATE TABLE PIPELINE] Could not create table to Postgres at 'postgres:5432/airflow'. "
                          f"Check if the container is up. Details: {e}")
        raise 


create_tables()