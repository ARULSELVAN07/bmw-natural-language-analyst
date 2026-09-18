from bmw_analyst.snowflake.connection import get_connection
from config.settings import SNOWFLAKE_DATABASE


def create_database():
    sql = f"""
    CREATE DATABASE IF NOT EXISTS {SNOWFLAKE_DATABASE}
    """

    connection = get_connection(use_database=False)

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
    finally:
        connection.close()

    print(f"Database ready: {SNOWFLAKE_DATABASE}")