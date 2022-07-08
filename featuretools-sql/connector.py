import warnings

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
            "mysql+pymysql", user, password, host, database=database
        )
        self.engine = None
        self.connection = None
        self.connect()

        self.relationships = []
        self.tables = []
        self.dataframes = dict()

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

    def all_tables(self):
        df = pd.read_sql("SHOW TABLES;", self.connection)
        return df

    def learn_table_schema(self, table: str):
        df = pd.read_sql(f"DESCRIBE {table};", self.connection)
        return df

    def get_table(self, table: str):
        df = pd.read_sql(f"SELECT * FROM {table}", self.connection)
        return df

    def get_primary_key_from_table(self, table: str):
        df = pd.read_sql(
            f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY';", self.connection
        )
        warnings.warn("Cannot handle composite keys yet!")
        return df["Column_name"]

    def populate_dataframes(self, debug=False):
        tables_df = self.all_tables()
        db = self.config["database"]
        table_index = f"Tables_in_{db}"
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
        df = pd.read_sql(query, self.connection)
        return df
