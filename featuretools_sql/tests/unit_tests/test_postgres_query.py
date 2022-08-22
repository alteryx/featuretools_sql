import os

import pytest
from featuretools import EntitySet

from featuretools_sql.connector import DBConnector

# Environment variable
# -> determine which DBMS is being tested


""""
TODO:
    1) Set up mock data structures for testing what is currently in unit_test (use Mock)
        (a) Main point here is that the user doesn't need to setup actual instance of DB
    2) Copy these tests (not mocked) to integration_tests
        (b) These would be called in the GitHub workflow with an actual instance of DB
    3) Postgres integration test would be able to be run
    4) Keep integration tests in GitHub workflow with Docker

"""


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

    print(os.getenv("POSTGRESURL"))

    return config


def test_can_connect_to_postgres(postgres_connection):
    DBConnector(**postgres_connection)


def test_can_get_all_tables(postgres_connection):
    c = DBConnector(**postgres_connection)
    df = c.all_tables()
    print(f"df: {df}")
    assert df is not None


def test_can_learn_dataframes(postgres_connection):
    c = DBConnector(**postgres_connection)
    c.populate_dataframes(debug=False)
    es = EntitySet("es", c.dataframes, [])
    assert es is not None


def test_can_get_relationships(postgres_connection):
    sql_connection = DBConnector(**postgres_connection)
    sql_connection.populate_dataframes()
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    print(f"df: {es.dataframes}")
    print(f"relationships: {es.relationships}")
    assert es is not None
