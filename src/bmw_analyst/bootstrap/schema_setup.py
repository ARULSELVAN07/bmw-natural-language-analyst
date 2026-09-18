from bmw_analyst.snowflake.connection import get_connection
from config.settings import (
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
)


def create_schema():
    sql = f"""
    CREATE SCHEMA IF NOT EXISTS
    {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}
    """

    connection = get_connection(use_database=False)

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
    finally:
        connection.close()

    print(
        f"Schema ready: "
        f"{SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}"
    )