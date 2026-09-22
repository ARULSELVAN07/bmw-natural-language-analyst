Security
========

Security Overview
-----------------

The BMW Natural Language Data Analyst uses multiple controls to protect
the analytical data layer.

Read-Only Database Role
-----------------------

The application uses the configured read-only Snowflake role::

    BMW_ANALYST_READONLY

SQL Validation
--------------

Generated SQL is validated before it is executed.

The allowed SQL command is:

::

    SELECT

Blocked SQL Commands
--------------------

The validator blocks commands including:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* TRUNCATE
* CREATE
* MERGE
* GRANT
* REVOKE

Approved Tables
---------------

Only approved BMW analytical tables are allowed:

* ``BMW_VEHICLE_SALES``
* ``BMW_WARRANTY``
* ``BMW_FAULTS``
* ``BMW_BATTERY``

Query Limits
------------

The application applies a maximum result limit of 1000 rows.

Query Timeout
-------------

Queries have a configured timeout of 30 seconds.

Question Length
---------------

Incoming questions are limited to 1000 characters.

Audit Logging
-------------

Application logging records query execution status.

Sensitive credentials and passwords should not be written to logs.

Credential Protection
---------------------

Credentials should be supplied through environment variables or an
appropriate secrets-management mechanism.

The ``.env`` file must not be committed to source control.

Security Testing
----------------

Security tests verify:

* Approved SELECT statements.
* Rejection of destructive SQL.
* Approved-table restrictions.
* Query-limit behavior.
* Configuration limits.
