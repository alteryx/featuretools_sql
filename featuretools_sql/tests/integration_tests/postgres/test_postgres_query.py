import pytest
from featuretools import EntitySet

from featuretools_sql.connector import DBConnector


@pytest.fixture
def postgres_connection():
    config = dict()
    config["system_name"] = "postgresql"
    config["host"] = "127.0.0.1"
    config["port"] = "5432"
    config["password"] = "postgres"
    config["user"] = "postgres"
    config["database"] = "postgres"
    config["schema"] = "public"
    return config


def test_can_connect_to_postgres(postgres_connection):
    DBConnector(**postgres_connection)


def test_can_get_all_tables(postgres_connection):
    c = DBConnector(**postgres_connection)
    df = c.all_tables()
    assert len(df) == 3


def test_can_learn_dataframes_and_relationships(postgres_connection):
    sql_connection = DBConnector(**postgres_connection)
    sql_connection.populate_dataframes(select_only=["products", "transactions"])
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    assert es is not None
    assert sorted(df.ww.name for df in es.dataframes) == ["products", "transactions"]
    assert len(es.relationships) == 1


def test_can_learn_dataframes_and_relationships_select_one(postgres_connection):
    sql_connection = DBConnector(**postgres_connection)
    sql_connection.populate_dataframes(select_only=["products"])
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    assert es is not None
    assert sorted(df.ww.name for df in es.dataframes) == ["products"]
    assert len(es.relationships) == 0
