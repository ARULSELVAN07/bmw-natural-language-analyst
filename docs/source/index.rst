BMW Natural Language Data Analyst
=================================

Welcome to the documentation for the BMW Natural Language Data Analyst.

This project allows BMW business users to ask analytical questions using
natural language instead of manually writing SQL queries.

Example Questions
------------------

* Which BMW model had the highest warranty cost in Chennai?
* Which BMW model had the highest vehicle sales?
* What are the most common BMW faults?
* What is the current battery status?

Architecture
------------

::

    User
      |
      v
    Streamlit UI
      |
      v
    FastAPI
      |
      v
    Agent
      |
      v
    Intent Router
      |
      v
    SQL Generator
      |
      v
    SQL Validator
      |
      v
    MCP Server
      |
      v
    Snowflake
      |
      v
    Query Result
      |
      v
    Narrative Explanation

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   architecture
   installation
   configuration
   mcp
   snowflake
   security
   api
   testing
   terraform
   project_structure

Key Features
------------

* Natural-language BMW analytics
* MCP-based tool architecture
* Amazon Bedrock integration
* Snowflake integration
* Read-only database access
* SQL validation
* Approved-table restrictions
* Query row limits
* Query timeout protection
* Audit logging
* FastAPI API
* Streamlit interface
* Automated testing

Technology Stack
----------------

* Python 3.12
* FastAPI
* Streamlit
* Model Context Protocol
* Amazon Bedrock
* Snowflake
* Pytest
* Sphinx

Project Status
--------------

The project provides a natural-language interface for querying approved
BMW analytical data while enforcing read-only SQL access.
