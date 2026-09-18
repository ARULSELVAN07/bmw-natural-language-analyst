from typing import Any

from .connection import get_connection


def execute_query(
    sql: str,
    params: tuple[Any, ...] | None = None,
) -> list[dict[str, Any]]:
    connection = get_connection()

    try:
        cursor = connection.cursor()

        try:
            cursor.execute(sql, params)

            columns = [column[0] for column in cursor.description]

            rows = cursor.fetchall()

            return [
                dict(zip(columns, row))
                for row in rows
            ]

        finally:
            cursor.close()

    finally:
        connection.close()