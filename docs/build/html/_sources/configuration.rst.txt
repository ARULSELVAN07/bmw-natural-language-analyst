Configuration
=============

Overview
--------

The application uses environment variables for runtime configuration.

Snowflake Configuration
-----------------------

Required Snowflake settings include::

    SNOWFLAKE_ACCOUNT
    SNOWFLAKE_USER
    SNOWFLAKE_PASSWORD
    SNOWFLAKE_AUTHENTICATOR
    SNOWFLAKE_ROLE
    SNOWFLAKE_WAREHOUSE
    SNOWFLAKE_DATABASE
    SNOWFLAKE_SCHEMA

AWS Configuration
-----------------

AWS and Amazon Bedrock settings include::

    AWS_REGION
    BEDROCK_MODEL_ID

Application Configuration
-------------------------

Application settings include::

    API_HOST
    API_PORT
    STREAMLIT_HOST
    STREAMLIT_PORT
    MCP_SERVER_NAME
    APP_NAME
    LOG_LEVEL

Example Configuration
---------------------

Use placeholders in documentation rather than real credentials::

    SNOWFLAKE_ACCOUNT=<account>
    SNOWFLAKE_USER=<username>
    SNOWFLAKE_PASSWORD=<password>
    SNOWFLAKE_AUTHENTICATOR=snowflake
    SNOWFLAKE_ROLE=BMW_ANALYST_READONLY
    SNOWFLAKE_WAREHOUSE=BMW_WH
    SNOWFLAKE_DATABASE=BMW_ANALYTICS
    SNOWFLAKE_SCHEMA=BMW_DATA

    AWS_REGION=ap-south-1
    BEDROCK_MODEL_ID=<bedrock-model-id>

    API_HOST=127.0.0.1
    API_PORT=8000

    STREAMLIT_HOST=127.0.0.1
    STREAMLIT_PORT=8501

    MCP_SERVER_NAME=BMW Natural Language Analyst
    APP_NAME=BMW Natural Language Data Analyst
    LOG_LEVEL=INFO

Approved Tables
---------------

The application uses the following approved analytical tables:

* ``BMW_VEHICLE_SALES``
* ``BMW_WARRANTY``
* ``BMW_FAULTS``
* ``BMW_BATTERY``

Operational Limits
------------------

Maximum query rows::

    1000

Query timeout::

    30 seconds

Maximum question length::

    1000 characters

Environment Security
--------------------

The ``.env`` file contains sensitive configuration and must not be committed
to Git.

Use ``.gitignore`` to exclude environment files from source control.
