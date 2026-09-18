import re

from config.settings import APPROVED_TABLES, BLOCKED_SQL_COMMANDS


def validate_sql(sql: str) -> bool:
    """
    Validate SQL before execution.

    Only single-statement SELECT queries against approved
    BMW tables are allowed.
    """

    if not sql or not sql.strip():
        return False

    sql = sql.strip()

    # Remove trailing semicolon
    if sql.endswith(";"):
        sql = sql[:-1].strip()

    # Reject multiple SQL statements
    if ";" in sql:
        return False

    # Only SELECT statements
    if not re.match(r"^SELECT\b", sql, re.IGNORECASE):
        return False

    # Reject dangerous SQL commands
    for command in BLOCKED_SQL_COMMANDS:
        if re.search(
            rf"\b{re.escape(command)}\b",
            sql,
            re.IGNORECASE,
        ):
            return False

    # Check that at least one approved table is referenced
    approved_table_found = False

    for table in APPROVED_TABLES:
        if re.search(
            rf"\b{re.escape(table)}\b",
            sql,
            re.IGNORECASE,
        ):
            approved_table_found = True
            break

    if not approved_table_found:
        return False

    return True