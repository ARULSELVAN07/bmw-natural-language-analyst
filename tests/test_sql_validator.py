from bmw_analyst.security.sql_validator import validate_sql


def test_valid_select():

    sql = """
    SELECT
        model,
        SUM(sales_amount) AS total_sales
    FROM BMW_VEHICLE_SALES
    GROUP BY model
    """

    assert validate_sql(sql) is True


def test_reject_insert():

    sql = """
    INSERT INTO BMW_VEHICLE_SALES
    VALUES (1, 'BMW X1', 'Chennai', '2026-01-01', 5000000, 1)
    """

    assert validate_sql(sql) is False


def test_reject_update():

    sql = """
    UPDATE BMW_VEHICLE_SALES
    SET sales_amount = 0
    """

    assert validate_sql(sql) is False


def test_reject_delete():

    sql = """
    DELETE FROM BMW_VEHICLE_SALES
    """

    assert validate_sql(sql) is False


def test_reject_drop():

    sql = """
    DROP TABLE BMW_VEHICLE_SALES
    """

    assert validate_sql(sql) is False


def test_reject_unapproved_table():

    sql = """
    SELECT *
    FROM CUSTOMER_DATA
    """

    assert validate_sql(sql) is False


def test_reject_multiple_statements():

    sql = """
    SELECT *
    FROM BMW_VEHICLE_SALES;

    DROP TABLE BMW_VEHICLE_SALES
    """

    assert validate_sql(sql) is False