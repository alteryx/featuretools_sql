# TODO: Actually compare the results to something

"""
Are these 'unit tests'?
More of integration tests

Mock database
"""


import pytest
from featuretools import EntitySet

from featuretools_sql.connector import DBConnector


@pytest.fixture
def mysql_connection():
    config = dict()
    config["system_name"] = "mysql"
    config["host"] = "127.0.0.1"
    config["port"] = "3306"
    config["password"] = "password"
    config["user"] = "root"
    config["database"] = "dummy"
    return config


def test_can_connect_to_dummy_db(mysql_connection):
    DBConnector(**mysql_connection)


def test_faulty_connection_fails():
    with pytest.raises(ValueError):
        DBConnector(None, None, None, None, None, None)


# def test_can_run_query(mysql_connection):
#     c = DBConnector(**mysql_connection)
#     c._DBConnector__run_query(
#         "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{c.database}'"
#     )


def test_can_get_all_tables(mysql_connection):
    c = DBConnector(**mysql_connection)
    df = c.all_tables()
    assert df is not None


def test_can_learn_dataframes(mysql_connection):
    c = DBConnector(**mysql_connection)
    c.populate_dataframes(debug=False)
    es = EntitySet("es", c.dataframes, [])
    assert es is not None
    assert 2 == len(es.dataframes)


def test_can_learn_dataframes_and_relationships(mysql_connection):
    sql_connection = DBConnector(**mysql_connection)
    sql_connection.populate_dataframes()
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    assert es is not None
    assert sorted(df.ww.name for df in es.dataframes) == ["products", "transactions"]
    assert len(es.relationships) == 1
