import pytest
from featuretools import EntitySet

from featuretools_sql.connector import DBConnector


@pytest.fixture
def mysql_connection():
    config = dict()
    config["system_name"] = "mysql"
    config["host"] = "127.0.0.1"
    config["port"] = "8888"
    config["password"] = "password"
    config["user"] = "root"
    config["database"] = "db"
    return config


def test_can_connect_to_dummy_db(mysql_connection):
    DBConnector(**mysql_connection)


def test_faulty_connection_fails():
    with pytest.raises(NotImplementedError):
        DBConnector(None, None, None, None, None, None)


def test_can_get_all_tables(mysql_connection):
    c = DBConnector(**mysql_connection)
    df = c.all_tables()
    assert len(df) == 3


def test_can_learn_dataframes(mysql_connection):
    c = DBConnector(**mysql_connection)
    c.populate_dataframes()
    es = EntitySet("es", c.dataframes, [])
    assert es is not None
    assert len(es.dataframes) == 3


@pytest.mark.parametrize(
    "select_only, expected_dataframe_names, expected_relationship_length",
    [
        (None, ["products", "testtable", "transactions"], 2),
        (["PRODUCTS", "TESTTABLE"], ["products", "testtable"], 1),
        (["PRODUCTS", "TRANSACTIONS"], ["products", "transactions"], 1),
        (["PRODUCTS"], ["products"], 0),
    ],
)
def test_can_learn_dataframes_and_relationships(
    mysql_connection,
    select_only,
    expected_dataframe_names,
    expected_relationship_length,
):
    sql_connection = DBConnector(**mysql_connection)
    sql_connection.populate_dataframes(select_only=select_only)
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    assert es is not None
    assert (
        sorted(df.ww.name.lower() for df in es.dataframes) == expected_dataframe_names
    )
    assert len(es.relationships) == expected_relationship_length


def test_invalid_argument_populate_dataframes(mysql_connection):
    sql_connection = DBConnector(**mysql_connection)
    with pytest.raises(ValueError):
        sql_connection.populate_dataframes(select_only="PRODUCTS")
