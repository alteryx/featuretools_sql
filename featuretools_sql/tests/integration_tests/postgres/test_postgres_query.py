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


@pytest.mark.parametrize(
    "select_only, expected_dataframe_names, expected_relationship_length",
    [
        (None, ["products", "testtable", "transactions"], 2),
        (["products", "testtable"], ["products", "testtable"], 1),
        (["products", "transactions"], ["products", "transactions"], 1),
        (["products"], ["products"], 0),
    ],
)
def test_can_learn_dataframes_and_relationships(
    postgres_connection,
    select_only,
    expected_dataframe_names,
    expected_relationship_length,
):
    sql_connection = DBConnector(**postgres_connection)
    sql_connection.populate_dataframes(select_only=select_only)
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    assert es is not None
    assert (
        sorted(df.ww.name.lower() for df in es.dataframes) == expected_dataframe_names
    )
    assert len(es.relationships) == expected_relationship_length


def test_invalid_argument_populate_dataframes(postgres_connection):
    sql_connection = DBConnector(**postgres_connection)
    with pytest.raises(ValueError):
        sql_connection.populate_dataframes(select_only="PRODUCTS")
