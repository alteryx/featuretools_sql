#TODO: Fix imports 
#TODO: Actually compare the results to something

import pytest 
from ...connector import DBConnector
from featuretools import EntitySet


@pytest.fixture
def mysql_connection():
    config = dict()
    config["system_name"] = "mysql"
    config["host"] = "127.0.0.1"
    config["port"] = "3306"
    config["password"] = "harrypotter"
    config["user"] = "root"
    config["database"] = "dummy"
    return config


@pytest.fixture
def postgres_connection():
    config = dict()
    config["system_name"] = "postgresql"
    config["host"] = "127.0.0.1"
    config["port"] = "5432"
    config["password"] = "s"
    config["user"] = "postgres"
    config["database"] = "dummy"
    config["schema"] = "public"
    return config


@pytest.fixture
def expected_entity_set():
    dataframes = {}
    relationships = []
    es = EntitySet(dataframes=dataframes, relationships=relationships)


def test_can_connect_to_dummy_db(mysql_connection):
    DBConnector(**mysql_connection)


def test_can_connect_to_postgres(postgres_connection):
    DBConnector(**postgres_connection)


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


def test_can_get_all_tables(postgres_connection):
    c = DBConnector(**postgres_connection)
    df = c.all_tables()
    assert df is not None


def test_can_learn_dataframes(mysql_connection):
    c = DBConnector(**mysql_connection)
    c.populate_dataframes(debug=False)
    es = EntitySet("es", c.dataframes, [])
    assert es is not None


def test_can_learn_dataframes(postgres_connection):
    c = DBConnector(**postgres_connection)
    df = c.populate_dataframes(debug=False)
    es = EntitySet("es", c.dataframes, [])
    assert es is not None


def test_can_get_relationships(mysql_connection):
    sql_connection = DBConnector(**mysql_connection)
    sql_connection.populate_dataframes()
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    assert es is not None


def test_can_get_relationships(postgres_connection):
    sql_connection = DBConnector(**postgres_connection)
    sql_connection.populate_dataframes()
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    assert es is not None
