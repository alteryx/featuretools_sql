import pytest
from connector import DBConnector
from featuretools import EntitySet


@pytest.fixture
def my_dummy_connection():
    config = dict()
    config["system_name"] = "mysql"
    config["host"] = "127.0.0.1:3306"
    config["password"] = "harrypotter"
    config["user"] = "root"
    config["database"] = "dummy"
    c = DBConnector(**config) 
    c.run_query("CREATE TABLE PRODUCTS(id INT, transaction_id INT, PRIMARY KEY (id));")  
    c.run_query("CREATE TABLE TRANSACTIONS(transaction_id INT, product_id INT, PRIMARY KEY (transaction_id));") 
    return config


def test_can_connect_to_dummy_db(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)

def test_faulty_connection_fails():
    with pytest.raises(ValueError) as ve:
        c = DBConnector(None, None, None, None, None)


def test_can_run_query(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)
    c.run_query(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{c.database}'"
    )


def test_can_learn_schema(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)
    df = c.all_tables()


def test_can_learn_dataframes(my_dummy_connection):
    c = DBConnector(**my_dummy_connection)
    c.populate_dataframes(debug=False)
    es = EntitySet("es", c.dataframes, [])


def test_can_get_relationships(my_dummy_connection):
    sql_connection = DBConnector(**my_dummy_connection)
    sql_connection.populate_dataframes()
    sql_connection.populate_relationships()
    es = EntitySet("es", sql_connection.dataframes, sql_connection.relationships)
    print(f"Entity Set: {es}")
