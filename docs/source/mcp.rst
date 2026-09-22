MCP
===

Overview
--------

The Model Context Protocol (MCP) provides the controlled tool interface
between the BMW analyst agent and the data-access layer.

The MCP architecture separates natural-language reasoning from database
execution.

MCP Server
----------

The MCP server implementation is located at::

    src/bmw_analyst/mcp_server/server.py

Available Tools
---------------

Vehicle Sales
~~~~~~~~~~~~~

``get_vehicle_sales``

Provides access to BMW vehicle sales analysis.

Warranty Cost
~~~~~~~~~~~~~

``get_warranty_cost``

Provides access to BMW warranty-cost analysis.

Fault Summary
~~~~~~~~~~~~~

``get_fault_summary``

Provides access to BMW fault analysis.

Battery Status
~~~~~~~~~~~~~~

``get_battery_status``

Provides access to BMW battery analysis.

Approved Query Execution
~~~~~~~~~~~~~~~~~~~~~~~~

``execute_approved_query``

Executes SQL only after the application's SQL validation rules have
approved the query.

MCP Client
----------

The MCP client implementation is located at::

    src/bmw_analyst/mcp_client/client.py

The client starts the MCP server and invokes the required tool.

Execution Flow
--------------

::

    User Question
         |
         v
    Intent Detection
         |
         v
    SQL Generation
         |
         v
    SQL Validation
         |
         v
    MCP Client
         |
         v
    MCP Server
         |
         v
    Snowflake

Security
--------

MCP does not provide unrestricted database access.

SQL must pass the application's validation layer before execution.

The MCP layer therefore acts as a controlled interface between the
application and approved analytical operations.
