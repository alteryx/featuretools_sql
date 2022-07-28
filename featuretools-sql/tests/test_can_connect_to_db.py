import pytest
from connector import DBConnector
from featuretools import EntitySet

"""
TODO: Create mock fixtures to actually test equality 
"""

@pytest.fixture
def dummy_mysql_connection():
    config = dict()
    config["system_name"] = "mysql"
    config["host"] = "127.0.0.1:3306"
    config["password"] = "harrypotter"
    config["user"] = "root"
    config["database"] = "dummy"
    return config

@pytest.fixture
def dummy_postgres_connection(): 
    config = dict()
    config["system_name"] = "postgresql"
    config["host"] = "127.0.0.1:5432"
    config["password"] = "s"
    config["user"] = "shripad.badithe"
    config["database"] = "dummy"
    return config 

def test_can_connect_to_dummy_db(dummy_mysql_connection):
    DBConnector(**dummy_postgres_connection)


def test_can_connect_to_dummy_db(dummy_postgres_connection):
    c = DBConnector(**dummy_postgres_connection)


def test_faulty_connection_fails():
    with pytest.raises(ValueError):
        DBConnector(None, None, None, None, None)


def test_can_run_query(dummy_mysql_connection):
    c = DBConnector(**dummy_mysql_connection)
    c._DBConnector__run_query(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{c.database}'"
    )


def test_can_learn_schema(dummy_mysql_connection):
    c = DBConnector(**dummy_mysql_connection)
    df = c.all_tables()
    assert df is not None


def test_can_learn_schema_postgres(dummy_postgres_connection):
    c = DBConnector(**dummy_postgres_connection)
    df = c.all_tables()
    print(df) 


def test_can_learn_dataframes(dummy_mysql_connection):
    c = DBConnector(**dummy_mysql_connection)
    c.populate_dataframes(debug=False)
    es = EntitySet("es", c.dataframes, [])
    assert es is not None


def test_can_get_relationships(dummy_mysql_connection):
    sql_connection = DBConnector(**dummy_mysql_connection)
    sql_connection.populate_dataframes()
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    assert es is not None
