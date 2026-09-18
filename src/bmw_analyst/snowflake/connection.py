import snowflake.connector

from config.settings import get_snowflake_config


def get_connection(use_database: bool = True):
    config = get_snowflake_config()

    connection_config = {
        "account": config["account"],
        "user": config["user"],
        "password": config["password"],
        "authenticator": config["authenticator"],
        "role": config["role"],
        "disable_arrow": True,
    }

    if use_database:
        connection_config.update({
            "warehouse": config["warehouse"],
            "database": config["database"],
            "schema": config["schema"],
        })

    return snowflake.connector.connect(**connection_config)