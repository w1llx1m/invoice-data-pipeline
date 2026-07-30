from airflow.decorators import dag, task
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd


from scripts.extract import extract
from scripts.validate import validated_split
from scripts.transform import capitalize_columns, email_format, blank_removal
from scripts.load import get_engine, load_data
from database.init_db import create_tables


default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

@dag(
    dag_id="invoice_data_pipeline",
    schedule="@daily",
    start_date=datetime(2026, 7, 1),
    catchup=False,
    default_args=default_args,
    tags=["invoices"],
)
def invoice_pipeline():

    @task
    def create_tables_task():
        create_tables() 

    @task
    def extract_task() -> str:
        df = extract()
        output_path = "/opt/airflow/data/interim/extracted.csv"
        df.to_csv(output_path, index=False)
        return output_path  # só o CAMINHO vai pelo XCom, não o DataFrame inteiro

    @task
    def validate_and_split_task(input_path: str) -> dict:
        df = pd.read_csv(input_path)
        mask_approved = validated_split(df)

        df_approved = df[mask_approved].copy()
        df_reproved = df[~mask_approved].copy()

        approved_path = "/opt/airflow/data/interim/approved.csv"
        reproved_path = "/opt/airflow/data/interim/reproved.csv"

        df_approved.to_csv(approved_path, index=False)
        df_reproved.to_csv(reproved_path, index=False)

        return {"approved": approved_path, "reproved": reproved_path}

    @task
    def transform_task(paths: dict) -> str:
        df = pd.read_csv(paths["approved"])

        df = capitalize_columns(df)
        df = email_format(df)
        df = blank_removal(df)

        transformed_path = "/opt/airflow/data/interim/transformed.csv"
        df.to_csv(transformed_path, index=False)
        return transformed_path

    @task
    def load_task(transformed_path: str):
        df = pd.read_csv(transformed_path)
        engine = get_engine()
        load_data(df, engine, table_name="invoices")

    # --- Orquestração: define a ordem/dependência entre as tasks ---
    create_tables_task()
    extracted = extract_task()

    create_tables_task() >> extracted
    split_paths = validate_and_split_task(extracted)
    transformed = transform_task(split_paths)
    load_task(transformed)


invoice_pipeline()