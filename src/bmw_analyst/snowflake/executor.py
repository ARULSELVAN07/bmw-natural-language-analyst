import re
from typing import Any

from config.settings import (
    MAX_QUERY_ROWS,
    QUERY_TIMEOUT_SECONDS,
)

from bmw_analyst.security.logging_config import logger

from .connection import get_connection


def apply_query_limit(sql: str) -> str:
    """
    Ensure the SQL query has a safe maximum row limit.
    """

    sql = sql.strip().rstrip(";").strip()

    if re.search(r"\bLIMIT\s+\d+\b", sql, re.IGNORECASE):
        return sql

    return f"{sql}\nLIMIT {MAX_QUERY_ROWS}"


def execute_query(
    sql: str,
    params: tuple[Any, ...] | None = None,
) -> list[dict[str, Any]]:
    logger.info("Snowflake query execution started")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        try:
            safe_sql = apply_query_limit(sql)

            logger.info(
                "Executing Snowflake query with max_rows=%s timeout=%s",
                MAX_QUERY_ROWS,
                QUERY_TIMEOUT_SECONDS,
            )

            cursor.execute(
                safe_sql,
                params,
                timeout=QUERY_TIMEOUT_SECONDS,
            )

            columns = [column[0] for column in cursor.description]

            rows = cursor.fetchmany(MAX_QUERY_ROWS)

            result = [
                dict(zip(columns, row))
                for row in rows
            ]

            logger.info(
                "Snowflake query completed successfully rows_returned=%s",
                len(result),
            )

            return result

        except Exception:
            logger.exception("Snowflake query execution failed")
            raise

        finally:
            cursor.close()

    finally:
        connection.close()
        logger.info("Snowflake connection closed")