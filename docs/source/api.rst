API
===

Overview
--------

The BMW Natural Language Data Analyst exposes a FastAPI service for
natural-language BMW analysis.

API Implementation
-------------------

The API implementation is located at::

    src/bmw_analyst/api/main.py

Ask Endpoint
------------

The main analytical endpoint is:

::

    POST /ask

Request
-------

The endpoint accepts a natural-language question.

Example request::

    {
        "question": "Which BMW model had the highest warranty cost in Chennai?"
    }

Response
--------

The response can contain:

* Original question
* Detected intent
* Generated SQL
* Query data
* Narrative answer

PowerShell Example
------------------

::

    $body = @{
        question = "Which BMW model had the highest warranty cost in Chennai?"
    } | ConvertTo-Json

    Invoke-RestMethod `
        -Uri "http://127.0.0.1:8000/ask" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body

FastAPI Documentation
---------------------

When the API is running, FastAPI provides interactive documentation at::

    http://127.0.0.1:8000/docs

ReDoc is available at::

    http://127.0.0.1:8000/redoc

API Workflow
------------

::

    HTTP Request
         |
         v
    Question Validation
         |
         v
    Agent
         |
         v
    MCP
         |
         v
    Snowflake
         |
         v
    Narrative Response
         |
         v
    HTTP Response
