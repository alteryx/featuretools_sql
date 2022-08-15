import pytest
from ..connector import DBConnector
from featuretools import EntitySet
import pandas as pd
import psycopg2
import unittest
import testing.postgresql

"""
TODO: Create mock fixtures to actually test equality 
"""


def load_dataframes_into_postgres(es, engine): 
    """ 
    Given an entityset and an engine, 
    load all the dataframes in the entity set into 
    the relational database. Also, set the primary keys
    """
    for df in es.dataframes:
        name = df.ww.name
        idx_col = df.ww.index   

        df.to_sql(name, engine, index=False)

        with engine.connect() as con:
            rs = con.execute(f'ALTER TABLE public.{name} add primary key ({idx_col})')
    

def test_populate_dataframes():
    """ 
    Launch new Postgres instance, load data from demo database
    Tests that `populate_dataframes` works correctly
    """
    with testing.postgresql.Postgresql() as postgresql:

        from sqlalchemy import create_engine
        import featuretools as ft

        engine = create_engine(postgresql.url())
        es = ft.demo.load_retail()  

        load_dataframes_into_postgres(es, engine)

        config = postgresql.dsn()
        config['system_name'] = 'postgresql'
        config['schema'] = 'public'

        connector = DBConnector(**config)

        dfs = connector.populate_dataframes()
        print(f"dataframes: {dfs}")


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

