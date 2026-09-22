import sys
from typing import Any

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from .models import MCPResponse


class MCPClient:

    def __init__(
        self,
        server_command: str | None = None,
        server_args: list[str] | None = None,
    ):
        self.server_command = server_command or sys.executable
        self.server_args = server_args or [
            "-m",
            "bmw_analyst.mcp_server.server",
        ]

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> MCPResponse:

        arguments = arguments or {}

        server_params = StdioServerParameters(
            command=self.server_command,
            args=self.server_args,
        )

        async with stdio_client(server_params) as streams:

            async with ClientSession(
                streams[0],
                streams[1],
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )

                data: list[dict[str, Any]] = []

                for content in result.content:

                    if hasattr(content, "text"):

                        import json

                        try:
                            parsed = json.loads(content.text)

                            if isinstance(parsed, dict):

                                if parsed.get("success") is False:
                                    return MCPResponse(
                                        success=False,
                                        tool=tool_name,
                                        error=parsed.get(
                                            "error",
                                            "MCP tool execution failed.",
                                        ),
                                    )

                                data = parsed.get(
                                    "data",
                                    [],
                                )

                        except json.JSONDecodeError:
                            pass

                return MCPResponse(
                    success=True,
                    tool=tool_name,
                    data=data,
                )

    async def get_vehicle_sales(self) -> MCPResponse:
        return await self.call_tool(
            "vehicle_sales"
        )

    async def get_warranty_cost(self) -> MCPResponse:
        return await self.call_tool(
            "warranty_cost"
        )

    async def get_fault_summary(self) -> MCPResponse:
        return await self.call_tool(
            "fault_summary"
        )

    async def get_battery_status(self) -> MCPResponse:
        return await self.call_tool(
            "battery_status"
        )

    async def execute_approved_query(
        self,
        sql: str,
    ) -> MCPResponse:

        return await self.call_tool(
            "execute_approved_query",
            {
                "sql": sql,
            },
        )