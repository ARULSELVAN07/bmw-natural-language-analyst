from bmw_analyst.snowflake.connection import get_connection
from config.settings import SNOWFLAKE_WAREHOUSE


def create_warehouse():
    sql = f"""
    CREATE WAREHOUSE IF NOT EXISTS {SNOWFLAKE_WAREHOUSE}
    WITH
        WAREHOUSE_SIZE = 'XSMALL'
        AUTO_SUSPEND = 60
        AUTO_RESUME = TRUE
        INITIALLY_SUSPENDED = TRUE
    """

    connection = get_connection(use_database=False)

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
    finally:
        connection.close()

    print(f"Warehouse ready: {SNOWFLAKE_WAREHOUSE}")