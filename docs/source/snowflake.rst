Snowflake
=========

Overview
--------

Snowflake is used as the analytical data warehouse for BMW data.

Database
--------

::

    BMW_ANALYTICS

Schema
------

::

    BMW_DATA

Warehouse
---------

::

    BMW_WH

Read-Only Role
--------------

The configured analytical role is::

    BMW_ANALYST_READONLY

Approved Tables
---------------

The application restricts analytical queries to:

* ``BMW_VEHICLE_SALES``
* ``BMW_WARRANTY``
* ``BMW_FAULTS``
* ``BMW_BATTERY``

Connection Module
-----------------

The Snowflake connection implementation is located at::

    src/bmw_analyst/snowflake/connection.py

Query Executor
--------------

The query executor is located at::

    src/bmw_analyst/snowflake/executor.py

Query Execution
---------------

The executor performs the following operations:

#. Open a Snowflake connection.
#. Execute validated SQL.
#. Apply the configured row limit.
#. Apply the configured query timeout.
#. Fetch the result.
#. Close the cursor.
#. Close the connection.
#. Record execution status.

Row Limit
---------

The maximum configured result size is:

::

    1000 rows

Query Timeout
-------------

The configured query timeout is:

::

    30 seconds

Read-Only Design
----------------

The application is designed for analytical read operations.

Database permissions and application-level SQL validation work together
to prevent data modification operations.
