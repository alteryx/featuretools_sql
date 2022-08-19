import testing.postgresql
from featuretools import demo

# TODO: Fix relative import
from featuretools_sql.connector import DBConnector
from featuretools_sql.tests.testing_utils import (
    add_foreign_key_postgres,
    load_dataframes_into_engine,
    verify_relationships_are_equal,
)


def test_populate_dataframes_and_populate_relationships():
    """
    Launch new Postgres instance, load data from demo database
    Tests that `populate_dataframes` works correctly
    """
    with testing.postgresql.Postgresql() as postgresql:

        from sqlalchemy import create_engine

        engine = create_engine(postgresql.url())
        es = demo.load_retail()

        load_dataframes_into_engine(es.dataframes, engine)

        with engine.connect() as con:
            add_foreign_key_postgres(
                con,
                "public.order_products",
                "fk",
                "product_id",
                "products",
                "product_id",
            )
            add_foreign_key_postgres(
                con, "public.order_products", "fk1", "order_id", "orders", "order_id"
            )
            add_foreign_key_postgres(
                con,
                "public.orders",
                "fk2",
                "customer_name",
                "customers",
                "customer_name",
            )

        config = postgresql.dsn()
        config["system_name"] = "postgresql"
        config["schema"] = "public"

        connector = DBConnector(**config)
        connector.populate_dataframes()

    verify_relationships_are_equal(connector.relationships, es.relationships)
    assert sorted(set(df.ww.name for df in es.dataframes)) == sorted(
        connector.dataframes.keys()
    )
