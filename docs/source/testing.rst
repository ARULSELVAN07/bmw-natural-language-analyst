Testing
=======

Overview
--------

The project uses Pytest for automated testing.

Run the Test Suite
------------------

From the project root::

    python -m pytest -q

Test Files
----------

API Tests
~~~~~~~~~

::

    tests/test_api.py

Tests FastAPI application behavior.

Agent Tests
~~~~~~~~~~~

::

    tests/test_agent.py

Tests natural-language analysis behavior.

MCP Client Tests
~~~~~~~~~~~~~~~~

::

    tests/test_mcp_client.py

Tests MCP client behavior.

MCP Tool Tests
~~~~~~~~~~~~~~

::

    tests/test_mcp_tools.py

Tests MCP tool functionality.

Router Tests
~~~~~~~~~~~~

::

    tests/test_router.py

Tests analytical intent routing.

SQL Validator Tests
~~~~~~~~~~~~~~~~~~~

::

    tests/test_sql_validator.py

Tests SQL safety rules.

Query Limit Tests
~~~~~~~~~~~~~~~~~

::

    tests/test_query_limits.py

Tests query-result limits.

Snowflake Tests
~~~~~~~~~~~~~~~

::

    tests/test_snowflake.py

Tests Snowflake-related functionality.

Security Testing
----------------

Security tests verify that destructive SQL statements are rejected.

Examples include:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* TRUNCATE

Continuous Integration
----------------------

The project contains a GitHub Actions workflow for automated testing.

The CI workflow:

#. Checks out the repository.
#. Installs Python 3.12.
#. Installs project dependencies.
#. Installs development dependencies.
#. Runs Pytest.

CI Security
-----------

Normal unit and security tests should not require production Snowflake
credentials.

Live database integration tests should be isolated when external
infrastructure is required.
