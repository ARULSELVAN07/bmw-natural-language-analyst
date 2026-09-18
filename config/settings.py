import os
from pathlib import Path
from dotenv import load_dotenv


# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


# -------------------------------------------------
# Environment Helpers
# -------------------------------------------------

def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' "
            f"is missing from {ENV_FILE}"
        )

    return value


# -------------------------------------------------
# Snowflake Configuration
# -------------------------------------------------

SNOWFLAKE_ACCOUNT = get_required_env("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = get_required_env("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = get_required_env("SNOWFLAKE_PASSWORD")
SNOWFLAKE_AUTHENTICATOR = get_required_env("SNOWFLAKE_AUTHENTICATOR")
SNOWFLAKE_ROLE = get_required_env("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = get_required_env("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = get_required_env("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = get_required_env("SNOWFLAKE_SCHEMA")


def get_snowflake_config() -> dict:
    return {
        "account": SNOWFLAKE_ACCOUNT,
        "user": SNOWFLAKE_USER,
        "password": SNOWFLAKE_PASSWORD,
        "authenticator": SNOWFLAKE_AUTHENTICATOR,
        "role": SNOWFLAKE_ROLE,
        "warehouse": SNOWFLAKE_WAREHOUSE,
        "database": SNOWFLAKE_DATABASE,
        "schema": SNOWFLAKE_SCHEMA,
    }


# -------------------------------------------------
# AWS / Bedrock Configuration
# -------------------------------------------------

AWS_REGION = get_required_env("AWS_REGION")
BEDROCK_MODEL_ID = get_required_env("BEDROCK_MODEL_ID")


# -------------------------------------------------
# API Configuration
# -------------------------------------------------

API_HOST = get_required_env("API_HOST")
API_PORT = int(get_required_env("API_PORT"))


# -------------------------------------------------
# Streamlit Configuration
# -------------------------------------------------

STREAMLIT_HOST = get_required_env("STREAMLIT_HOST")
STREAMLIT_PORT = int(get_required_env("STREAMLIT_PORT"))


# -------------------------------------------------
# Application Configuration
# -------------------------------------------------

MCP_SERVER_NAME = get_required_env("MCP_SERVER_NAME")
APP_NAME = get_required_env("APP_NAME")
LOG_LEVEL = get_required_env("LOG_LEVEL")


# -------------------------------------------------
# Approved Database Tables
# -------------------------------------------------

APPROVED_TABLES = {
    "BMW_VEHICLE_SALES",
    "BMW_WARRANTY",
    "BMW_FAULTS",
    "BMW_BATTERY",
}


# -------------------------------------------------
# Approved MCP Tools
# -------------------------------------------------

APPROVED_MCP_TOOLS = {
    "get_vehicle_sales",
    "get_warranty_cost",
    "get_fault_summary",
    "get_battery_status",
    "execute_approved_query",
}


# -------------------------------------------------
# SQL Security
# -------------------------------------------------

ALLOWED_SQL_COMMAND = "SELECT"

BLOCKED_SQL_COMMANDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "MERGE",
    "GRANT",
    "REVOKE",
}


# -------------------------------------------------
# Query Resource Protection
# -------------------------------------------------

MAX_QUERY_ROWS = 1000

QUERY_TIMEOUT_SECONDS = 30

MAX_QUESTION_LENGTH = 1000