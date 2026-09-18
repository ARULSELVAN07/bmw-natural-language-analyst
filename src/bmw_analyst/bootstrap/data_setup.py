import csv
from pathlib import Path

from bmw_analyst.snowflake.connection import get_connection
from config.settings import (
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data" / "sample"


def load_csv(
    cursor,
    filename: str,
    table_name: str,
    columns: list[str],
):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    full_table_name = (
        f"{SNOWFLAKE_DATABASE}."
        f"{SNOWFLAKE_SCHEMA}."
        f"{table_name}"
    )

    # Clear existing sample data
    cursor.execute(
        f"TRUNCATE TABLE {full_table_name}"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        rows = []

        for row in reader:
            rows.append(
                tuple(
                    row[column]
                    for column in columns
                )
            )

    placeholders = ", ".join(
        ["%s"] * len(columns)
    )

    column_list = ", ".join(columns)

    sql = f"""
        INSERT INTO {full_table_name}
        ({column_list})
        VALUES ({placeholders})
    """

    if rows:
        cursor.executemany(sql, rows)

    print(
        f"Loaded {len(rows)} rows into "
        f"{full_table_name}"
    )


def load_all_data():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # -------------------------------------------------
        # Vehicle Sales
        # -------------------------------------------------

        load_csv(
            cursor,
            "vehicle_sales.csv",
            "BMW_VEHICLE_SALES",
            [
                "vehicle_id",
                "model",
                "city",
                "sale_date",
                "sales_amount",
                "quantity",
            ],
        )

        # -------------------------------------------------
        # Warranty
        # -------------------------------------------------

        load_csv(
            cursor,
            "warranty.csv",
            "BMW_WARRANTY",
            [
                "vehicle_id",
                "model",
                "city",
                "warranty_date",
                "fault_type",
                "warranty_cost",
            ],
        )

        # -------------------------------------------------
        # Faults
        # -------------------------------------------------

        load_csv(
            cursor,
            "faults.csv",
            "BMW_FAULTS",
            [
                "vehicle_id",
                "model",
                "city",
                "fault_date",
                "fault_type",
                "severity",
            ],
        )

        # -------------------------------------------------
        # Battery
        # -------------------------------------------------

        load_csv(
            cursor,
            "battery.csv",
            "BMW_BATTERY",
            [
                "vehicle_id",
                "model",
                "city",
                "battery_date",
                "battery_percentage",
                "battery_status",
            ],
        )

        cursor.close()

    finally:
        connection.close()

    print("All BMW sample data loaded successfully.")