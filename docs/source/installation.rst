Installation
============

Prerequisites
-------------

The project requires:

* Windows
* Python 3.12
* Git
* Snowflake account
* AWS account
* Amazon Bedrock access

Project Directory
-----------------

The project is located at::

    C:\bmw-natural-language-analyst

Virtual Environment
-------------------

Create the virtual environment::

    python -m venv bmwvenv

Activate the environment::

    .\bmwvenv\Scripts\Activate.ps1

Install Dependencies
--------------------

Install runtime dependencies::

    python -m pip install -r requirements.txt

Install development dependencies::

    python -m pip install -e ".[dev]"

Environment Configuration
-------------------------

Create a ``.env`` file in the project root.

The environment file contains configuration for:

* Snowflake
* AWS
* Amazon Bedrock
* FastAPI
* Streamlit
* MCP

Never commit real credentials to source control.

Run FastAPI
-----------

From the project root::

    uvicorn bmw_analyst.api.main:app --host 127.0.0.1 --port 8000 --reload

The API is available at::

    http://127.0.0.1:8000

Run Streamlit
-------------

Open another terminal and activate the virtual environment.

Run::

    streamlit run ui\streamlit_app.py

The Streamlit application normally opens at::

    http://127.0.0.1:8501

Run Tests
---------

Run the complete test suite::

    python -m pytest -q

Build Documentation
-------------------

From the ``docs`` directory::

    python -m sphinx -b html source build\html

Open the generated documentation::

    start build\html\index.html
