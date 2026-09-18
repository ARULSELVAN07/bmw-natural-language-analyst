from bmw_analyst.snowflake.connection import get_connection
from config.settings import (
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
)


def create_tables():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # -------------------------------------------------
        # BMW VEHICLE SALES
        # -------------------------------------------------

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS
            {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.BMW_VEHICLE_SALES
            (
                vehicle_id INTEGER,
                model VARCHAR(100),
                city VARCHAR(100),
                sale_date DATE,
                sales_amount FLOAT,
                quantity INTEGER
            )
            """
        )

        # -------------------------------------------------
        # BMW WARRANTY
        # -------------------------------------------------

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS
            {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.BMW_WARRANTY
            (
                vehicle_id INTEGER,
                model VARCHAR(100),
                city VARCHAR(100),
                warranty_date DATE,
                fault_type VARCHAR(100),
                warranty_cost FLOAT
            )
            """
        )

        # -------------------------------------------------
        # BMW FAULTS
        # -------------------------------------------------

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS
            {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.BMW_FAULTS
            (
                vehicle_id INTEGER,
                model VARCHAR(100),
                city VARCHAR(100),
                fault_date DATE,
                fault_type VARCHAR(100),
                severity VARCHAR(50)
            )
            """
        )

        # -------------------------------------------------
        # BMW BATTERY
        # -------------------------------------------------

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS
            {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.BMW_BATTERY
            (
                vehicle_id INTEGER,
                model VARCHAR(100),
                city VARCHAR(100),
                battery_date DATE,
                battery_percentage FLOAT,
                battery_status VARCHAR(50)
            )
            """
        )

        cursor.close()

    finally:
        connection.close()

    print("BMW tables created successfully.")