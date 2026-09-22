Project Structure
=================

The main project structure is:

::

    bmw-natural-language-analyst/
    |
    +-- config/
    |   +-- settings.py
    |   +-- __init__.py
    |
    +-- src/
    |   +-- bmw_analyst/
    |       |
    |       +-- agent/
    |       |   +-- agent.py
    |       |   +-- router.py
    |       |   +-- sql_generator.py
    |       |   +-- prompts.py
    |       |
    |       +-- api/
    |       |   +-- main.py
    |       |
    |       +-- mcp_client/
    |       |   +-- client.py
    |       |   +-- models.py
    |       |
    |       +-- mcp_server/
    |       |   +-- server.py
    |       |   +-- tools.py
    |       |   +-- schemas.py
    |       |
    |       +-- snowflake/
    |       |   +-- connection.py
    |       |   +-- executor.py
    |       |   +-- queries.py
    |       |
    |       +-- security/
    |       |   +-- sql_validator.py
    |       |   +-- permissions.py
    |       |   +-- logging_config.py
    |       |
    |       +-- models/
    |           +-- schemas.py
    |
    +-- tests/
    |   +-- test_api.py
    |   +-- test_agent.py
    |   +-- test_mcp_client.py
    |   +-- test_mcp_tools.py
    |   +-- test_router.py
    |   +-- test_sql_validator.py
    |   +-- test_query_limits.py
    |   +-- test_snowflake.py
    |
    +-- ui/
    |   +-- streamlit_app.py
    |
    +-- terraform/
    |   +-- snowflake/
    |
    +-- data/
    |   +-- sample/
    |
    +-- logs/
    |
    +-- docs/
    |   +-- source/
    |   +-- build/
    |
    +-- .github/
    |   +-- workflows/
    |
    +-- .env
    +-- .gitignore
    +-- pyproject.toml
    +-- requirements.txt
    +-- run.py
    +-- README.md

Important Directories
---------------------

``src/bmw_analyst/agent/``
    Natural-language analysis workflow.

``src/bmw_analyst/mcp_server/``
    MCP server implementation and tools.

``src/bmw_analyst/mcp_client/``
    MCP client functionality.

``src/bmw_analyst/snowflake/``
    Snowflake connection and query execution.

``src/bmw_analyst/security/``
    SQL validation, permissions, and logging.

``tests/``
    Automated tests.

``ui/``
    Streamlit user interface.

``terraform/``
    Infrastructure-as-code configuration.

``docs/``
    Sphinx documentation source and generated HTML files.

Configuration Files
-------------------

``pyproject.toml``
    Project metadata and Python dependencies.

``requirements.txt``
    Runtime dependencies.

``.env``
    Local environment configuration and secrets. This file must not be
    committed to Git.

``.gitignore``
    Files excluded from source control.
