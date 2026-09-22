from mcp.server.fastmcp import FastMCP

from config.settings import MCP_SERVER_NAME

from bmw_analyst.security.permissions import is_tool_allowed
from bmw_analyst.security.sql_validator import validate_sql
from bmw_analyst.snowflake.executor import execute_query

from .tools import (
    get_vehicle_sales,
    get_warranty_cost,
    get_fault_summary,
    get_battery_status,
)


mcp = FastMCP(MCP_SERVER_NAME)


@mcp.tool()
def vehicle_sales() -> dict:
    """
    Get BMW vehicle sales data.
    """
    return get_vehicle_sales()


@mcp.tool()
def warranty_cost() -> dict:
    """
    Get BMW warranty cost data.
    """
    return get_warranty_cost()


@mcp.tool()
def fault_summary() -> dict:
    """
    Get BMW fault summary data.
    """
    return get_fault_summary()


@mcp.tool()
def battery_status() -> dict:
    """
    Get BMW battery status data.
    """
    return get_battery_status()


@mcp.tool()
def execute_approved_query(sql: str) -> dict:
    """
    Execute a dynamically generated BMW analytics query.

    Only read-only SELECT queries against approved BMW tables
    are allowed.
    """

    if not is_tool_allowed("execute_approved_query"):
        return {
            "success": False,
            "tool": "execute_approved_query",
            "error": "Tool is not approved.",
        }

    if not validate_sql(sql):
        return {
            "success": False,
            "tool": "execute_approved_query",
            "error": "SQL validation failed.",
        }

    try:
        data = execute_query(sql)

        return {
            "success": True,
            "tool": "execute_approved_query",
            "data": data,
        }

    except Exception as exc:
        return {
            "success": False,
            "tool": "execute_approved_query",
            "error": str(exc),
        }


if __name__ == "__main__":
    mcp.run()