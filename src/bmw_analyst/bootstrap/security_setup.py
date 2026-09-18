from bmw_analyst.snowflake.connection import get_connection
from config.settings import (
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
)


READ_ONLY_ROLE = "BMW_ANALYST_READONLY"


def setup_security():

    connection = get_connection(use_database=False)

    try:
        cursor = connection.cursor()

        # -------------------------------------------------
        # Create read-only role
        # -------------------------------------------------

        cursor.execute(
            f"""
            CREATE ROLE IF NOT EXISTS
            {READ_ONLY_ROLE}
            """
        )

        # -------------------------------------------------
        # Database access
        # -------------------------------------------------

        cursor.execute(
            f"""
            GRANT USAGE ON DATABASE
            {SNOWFLAKE_DATABASE}
            TO ROLE {READ_ONLY_ROLE}
            """
        )

        # -------------------------------------------------
        # Schema access
        # -------------------------------------------------

        cursor.execute(
            f"""
            GRANT USAGE ON SCHEMA
            {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}
            TO ROLE {READ_ONLY_ROLE}
            """
        )

        # -------------------------------------------------
        # Existing tables
        # -------------------------------------------------

        cursor.execute(
            f"""
            GRANT SELECT ON ALL TABLES IN SCHEMA
            {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}
            TO ROLE {READ_ONLY_ROLE}
            """
        )

        # -------------------------------------------------
        # Future tables
        # -------------------------------------------------

        cursor.execute(
            f"""
            GRANT SELECT ON FUTURE TABLES IN SCHEMA
            {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}
            TO ROLE {READ_ONLY_ROLE}
            """
        )

        cursor.close()

    finally:
        connection.close()

    print(
        f"Read-only role ready: {READ_ONLY_ROLE}"
    )