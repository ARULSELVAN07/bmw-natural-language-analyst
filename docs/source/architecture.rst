Architecture
============

Overview
--------

The BMW Natural Language Data Analyst converts business questions written in
natural language into controlled analytical queries.

The application separates the user interface, AI processing, MCP tools,
security validation, and database execution.

System Architecture
-------------------

::

    +----------------------+
    |        User          |
    | Natural Language     |
    +----------+-----------+
               |
               v
    +----------------------+
    |    Streamlit UI      |
    +----------+-----------+
               |
               v
    +----------------------+
    |       FastAPI        |
    |        /ask          |
    +----------+-----------+
               |
               v
    +----------------------+
    |        Agent         |
    +----------+-----------+
               |
        +------+------+
        |             |
        v             v
    Intent Router   Amazon Bedrock
        |             |
        +------+------+
               |
               v
    +----------------------+
    |    SQL Generator     |
    +----------+-----------+
               |
               v
    +----------------------+
    |    SQL Validator     |
    +----------+-----------+
               |
               v
    +----------------------+
    |      MCP Client      |
    +----------+-----------+
               |
               v
    +----------------------+
    |      MCP Server      |
    +----------+-----------+
               |
               v
    +----------------------+
    | Snowflake Executor   |
    +----------+-----------+
               |
               v
    +----------------------+
    |      Snowflake       |
    +----------------------+

Main Components
---------------

Agent
~~~~~

The agent coordinates the natural-language analysis workflow.

Responsibilities include:

* Validating the incoming question.
* Identifying analytical intent.
* Generating SQL.
* Validating generated SQL.
* Executing the approved query.
* Generating a natural-language explanation.

Intent Router
~~~~~~~~~~~~~

The router identifies the type of BMW analytical question.

Supported areas include:

* Vehicle sales
* Warranty cost
* Fault summary
* Battery status

SQL Generator
~~~~~~~~~~~~~

The SQL generator converts the identified user intent into SQL suitable
for the approved Snowflake schema.

SQL Validator
~~~~~~~~~~~~~

The validator checks generated SQL before execution.

MCP Client
~~~~~~~~~~

The MCP client communicates with the MCP server and invokes approved tools.

MCP Server
~~~~~~~~~~

The MCP server exposes BMW analytical tools and controlled query execution.

Snowflake Executor
~~~~~~~~~~~~~~~~~~

The executor manages Snowflake connections, query execution, result retrieval,
timeouts, and row limits.

Security Layer
~~~~~~~~~~~~~~

The security layer ensures that only approved read-only queries can reach
Snowflake.

End-to-End Flow
---------------

#. User enters a natural-language question.
#. FastAPI receives the request.
#. The agent validates the question.
#. The router determines the analytical intent.
#. Amazon Bedrock generates SQL.
#. The SQL validator checks the generated SQL.
#. The approved SQL is sent through MCP.
#. Snowflake executes the query.
#. Results are returned to the agent.
#. The agent generates a narrative explanation.
#. The API returns the response.
#. Streamlit displays the result.
