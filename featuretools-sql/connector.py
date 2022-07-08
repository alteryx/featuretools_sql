import warnings

import connectorx as cx
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


class DBConnector:
    def __init__(self, user: str, password: str, host: str, database: str):
        self.config = {
            "user": user,
            "password": password,
            "host": host,
            "database": database,
        }
        if None in [user, password, host, database]:
            raise ValueError("Cannot pass None as argument to DBConnector constructor")
        self.connection_string = URL.create(
            "mysql", user, password, host, database=database
        )
        self.connection_string = "mysql://root:harrypotter@127.0.0.1/dummy"
        self.engine = None
        self.connection = None
        # self.connect()

        self.relationships = []
        self.tables = []
        self.dataframes = dict()

    """
    def change_password(self, new_password: str):
        self.config["password"] = new_password
        self.connection_string = URL.create(
            "mysql+pymysql", user, password, host, database=database
        )

    def change_user(self, new_user: str):
        self.config["user"] = new_user
        self.connection_string = URL.create(
            "mysql+pymysql", user, password, host, database=database
        )

    def change_host(self, new_host: str):
        self.config["host"] = new_host
        self.connection_string = URL.create(
            "mysql+pymysql", user, password, host, database=database
        )

    def connect(self):
        self.engine = create_engine(self.connection_string)
        self.connection = self.engine.connect()
        return
    """

    def all_tables(self):
        db = self.config["database"]
        return self.run_query(
            f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db}';"
        )

    def learn_table_schema(self, table: str):
        schema = self.config["database"] 
        return self.run_query(f"SELECT COLUMN_NAME AS `Field`, COLUMN_TYPE AS `Type`, IS_NULLABLE AS `NULL`,  COLUMN_KEY AS `Key`, COLUMN_DEFAULT AS `Default`, EXTRA AS `Extra` FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}';")

    def get_table(self, table: str):
        return self.run_query(f"SELECT * FROM {table}")

    def get_primary_key_from_table(self, table: str):
        db = self.config["database"]
        df = self.run_query(
            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{db}' AND TABLE_NAME = '{table}' AND COLUMN_KEY = 'PRI';"
        )
        warnings.warn("Cannot handle composite keys yet!")
        print(f"df : {df}")
        return df["COLUMN_NAME"]

    def populate_dataframes(self, debug=False):
        tables_df = self.all_tables()
        print(
            f"Tables_df : {tables_df}. Tables_df_index: {tables_df.index}. Tables_df_values: {tables_df.values}"
        )
        db = self.config["database"]
        table_index = f"TABLE_NAME"
        for table in tables_df[table_index].values:
            self.tables.append(table)
            table_df = self.get_table(table)
            try:
                table_key = self.get_primary_key_from_table(table).values[0]
            except Exception:
                raise Exception(
                    "Haven't implemented support for composite primary keys yet!"
                )
            self.dataframes[table] = (table_df, table_key)
        if debug:
            for k, v in self.dataframes.items():
                print(f"Name: {k}")
                print(f"df: {v}")
                print()
        return self.dataframes

    def populate_relationships(self, debug=False):
        query_str = f"SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = '{self.config['database']}'"
        foreign_keys = self.run_query(query_str)
        for (
            table_name,
            col_name,
            _,
            referenced_table_name,
            referenced_column_name,
        ) in foreign_keys.values:
            rel_tuple = (
                referenced_table_name,
                referenced_column_name,
                table_name,
                col_name,
            )
            self.relationships.append(rel_tuple)
        return

    def run_query(self, query: str):
        if not isinstance(query, str):
            raise ValueError(f"Query must be of string type, not {type(query)}")
        df = cx.read_sql(self.connection_string, query)
        return df
