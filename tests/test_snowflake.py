from bmw_analyst.snowflake.connection import get_connection


def test_snowflake_connection():
    connection = get_connection(use_database=False)

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT CURRENT_USER(), CURRENT_ACCOUNT()"
        )

        result = cursor.fetchone()

        assert result is not None

    finally:
        connection.close()