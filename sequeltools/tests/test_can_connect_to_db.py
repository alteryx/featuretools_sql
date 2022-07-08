import pytest
from featuretools import EntitySet 

from ..connector import DBConnector


@pytest.fixture
def my_dummy_connection():
    config = dict()
    config["host"] = "127.0.0.1"
    config["password"] = "harrypotter"
    config["user"] = "root"
    config["database"] = "dummy"
    return config


def test_can_connect_to_dummy_db(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)


def test_faulty_connection_fails():
    with pytest.raises(ValueError) as ve:
        c = DBConnector(None, None, None, None)


def test_can_run_query(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)
    c.run_query("SHOW TABLES;")


def test_can_learn_schema(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)
    df = c.all_tables()


def test_can_learn_dataframes(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)
    c.populate_dataframes(debug=False)


def test_can_get_relationships(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)
    c.populate_dataframes()
    c.populate_relationships()

    es = EntitySet("es", c.dataframes, c.relationships) 
    print(f"Entity Set: {es}") 