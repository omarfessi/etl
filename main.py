import pandas as pd
import psycopg2
from typing import Dict, Optional
from sql_dml import date_table_insert
from sql_ddl import tables_creation_queries
from postgres_manager import create_database, connect_to_database
from config import file_path, sheet_name, dtype_dict, columns_renaming_mapping


def read_xl_with_opt(
    file_path: str,
    sheet_name: str,
    dtype_dict: Dict,
    columns_renaming_mapping: Optional[Dict] = None,
) -> pd.DataFrame:
    """Reads an Excel file with optional dtype and column renaming."""
    base = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        dtype=dtype_dict,
        usecols=lambda x: x.strip() in columns_renaming_mapping
        if columns_renaming_mapping
        else None,
    )
    if columns_renaming_mapping:
        base.rename(columns=lambda x: columns_renaming_mapping[x.strip()], inplace=True)
    return base


def process_date_and_insert_into_db(
    conn: psycopg2.extensions.connection, event_date: pd.Series
) -> None:
    """Processes event dates and inserts them into the database."""
    event_dataframe = pd.DataFrame(
        {
            "ts": event_date,
            "day": event_date.dt.day,
            "week": event_date.dt.isocalendar().week,
            "month": event_date.dt.month,
            "year": event_date.dt.year,
            "dayofweek": event_date.dt.dayofweek,
        }
    )

    try:
        with conn.cursor() as cursor:
            for _, row in event_dataframe.iterrows():
                print(f"Inserting {row.tolist()} into the date_event table...")
                cursor.execute(date_table_insert, row.tolist())
            conn.commit()
    except psycopg2.Error as e:
        print(f"❌ Database insertion error: {e}")
        conn.rollback()


def create_tables(conn: psycopg2.extensions.connection) -> None:
    """Creates database tables using predefined SQL queries."""
    try:
        with conn.cursor() as cursor:
            for query in tables_creation_queries:
                print(f"Executing: {query}")
                cursor.execute(query)
            conn.commit()
    except psycopg2.Error as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()


def main():
    print("🚀 ETL pipeline is starting...")

    create_database()

    conn = connect_to_database()
    if conn is None:
        print("❌ Database connection failed. Exiting...")
        return

    try:
        create_tables(conn)

        base_sheet_as_df = read_xl_with_opt(
            file_path, sheet_name, dtype_dict, columns_renaming_mapping
        )
        event_date = base_sheet_as_df[~base_sheet_as_df["date"].isna()]["date"]

        process_date_and_insert_into_db(conn, event_date)
        print("✅ ETL pipeline completed successfully!")

    finally:
        conn.close()
        print("🔌 Database connection closed.")


if __name__ == "__main__":
    main()
