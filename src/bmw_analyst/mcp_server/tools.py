from typing import Any

from bmw_analyst.snowflake.executor import execute_query
from bmw_analyst.security.permissions import is_tool_allowed
from bmw_analyst.security.sql_validator import validate_sql
from bmw_analyst.snowflake.queries import (
    VEHICLE_SALES_QUERY,
    WARRANTY_COST_QUERY,
    FAULT_SUMMARY_QUERY,
    BATTERY_STATUS_QUERY,
)

from .schemas import MCPToolResponse


def _execute_tool(tool_name: str, sql: str) -> MCPToolResponse:
    """
    Execute an approved read-only BMW analytics query.
    """

    # Check MCP tool permission
    if not is_tool_allowed(tool_name):
        return MCPToolResponse(
            success=False,
            tool=tool_name,
            error="Tool is not approved.",
        )

    # Check SQL security
    if not validate_sql(sql):
        return MCPToolResponse(
            success=False,
            tool=tool_name,
            error="SQL validation failed.",
        )

    try:
        data = execute_query(sql)

        return MCPToolResponse(
            success=True,
            tool=tool_name,
            data=data,
        )

    except Exception as exc:
        return MCPToolResponse(
            success=False,
            tool=tool_name,
            error=str(exc),
        )


def get_vehicle_sales() -> dict[str, Any]:
    """
    Get BMW vehicle sales data.
    """
    response = _execute_tool(
        "get_vehicle_sales",
        VEHICLE_SALES_QUERY,
    )

    return response.model_dump()


def get_warranty_cost() -> dict[str, Any]:
    """
    Get BMW warranty cost data.
    """
    response = _execute_tool(
        "get_warranty_cost",
        WARRANTY_COST_QUERY,
    )

    return response.model_dump()


def get_fault_summary() -> dict[str, Any]:
    """
    Get BMW fault summary data.
    """
    response = _execute_tool(
        "get_fault_summary",
        FAULT_SUMMARY_QUERY,
    )

    return response.model_dump()


def get_battery_status() -> dict[str, Any]:
    """
    Get BMW battery status data.
    """
    response = _execute_tool(
        "get_battery_status",
        BATTERY_STATUS_QUERY,
    )

    return response.model_dump()