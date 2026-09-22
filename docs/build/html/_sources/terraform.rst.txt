Terraform
=========

Overview
--------

Terraform configuration is maintained for infrastructure-as-code resources.

Terraform Directory
-------------------

The project Terraform configuration is located under::

    terraform/

Snowflake Terraform
-------------------

Snowflake-related Terraform configuration is located under::

    terraform/snowflake/

Terraform Workflow
------------------

Initialize Terraform::

    terraform init

Validate the configuration::

    terraform validate

Create an execution plan::

    terraform plan

Apply infrastructure changes::

    terraform apply

Infrastructure Safety
---------------------

Always review the Terraform plan before applying infrastructure changes.

Terraform state may contain sensitive infrastructure information and should
not be committed to source control when it contains sensitive data.

Credentials
-----------

Do not hard-code Snowflake, AWS, or other credentials in Terraform files.

Use appropriate environment variables or secure credential mechanisms.
