from collections import defaultdict, namedtuple

import connectorx as cx
import pandas as pd
import psycopg2

class DBConnector:
    Relationship = namedtuple(
        "Relationship",
        ["referenced_table_name", "referenced_column_name", "table_name", "col_name"],
    )

    system_to_API = {"postgresql": "psycopg2", "mysql": "ConnectorX"}
    supported_systems = ["postgresql", "mysql"]

    def __init__(
        self, system_name: str, user: str, password: str, host: str, port: str, database: str, schema=None
    ):
        self.system_name = system_name
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port 
        self.schema = schema

        # TODO: Password security
        if None in [user, password, host, port, database]:
            raise ValueError("Cannot pass None as argument to DBConnector constructor")
        if system_name not in DBConnector.supported_systems:
            raise NotImplementedError(
                f"DBConnector does not currently support {database}"
            )
        self.connection_string = f"{system_name}://{user}:{password}@{host}:{port}/{database}"
        self.relationships = []
        self.tables = []
        self.dataframes = dict()
        if system_name == "postgresql": 
            assert schema != None 
            conn_string = "host='{}' port={} dbname='{}' user={} password={}".format(host, port, database, user, password)
            self.postgres_connection = psycopg2.connect(conn_string) 


    def change_system_name(self, system_name: str):
        self.system_name = system_name

    def change_password(self, new_password: str):
        self.password = new_password

    def change_user(self, new_user: str):
        self.new_user = new_user

    def change_host(self, new_host: str):
        self.new_host = new_host

    def all_tables(self) -> pd.DataFrame:
        if self.system_name == "mysql":
            return self.__run_query(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database}';"
            )
        elif self.system_name == "postgresql": 
            return self.__run_query(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.schema}';"
            )

    def learn_table_schema(self, table: str) -> pd.DataFrame:
        schema = self.database
        if self.system_name == "mysql":
            self.__run_query(
                f"SELECT COLUMN_NAME AS `Field`, COLUMN_TYPE AS `Type`, IS_NULLABLE AS `NULL`,  COLUMN_KEY AS `Key`, COLUMN_DEFAULT AS `Default`, EXTRA AS `Extra` FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}';"
            )

    def get_table(self, table: str) -> pd.DataFrame:
        return self.__run_query(f"SELECT * FROM {table}")

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        db = self.database
        if self.system_name == "mysql":
            df = self.__run_query(
                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{db}' AND TABLE_NAME = '{table}' AND COLUMN_KEY = 'PRI';"
            )
            return df["COLUMN_NAME"]

    def populate_dataframes(self, debug=False):
        tables_df = self.all_tables()
        table_index = "TABLE_NAME"
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
        return

    def populate_relationships(self, debug=False):
        self.relationships = []
        if self.system_name == "mysql":
            query_str = f"SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = '{self.database}'"
        foreign_keys = self.__run_query(query_str)
        for (
            table_name,
            col_name,
            _,
            referenced_table_name,
            referenced_column_name,
        ) in foreign_keys.values:
            r = DBConnector.Relationship(
                referenced_table_name,
                referenced_column_name,
                table_name,
                col_name,
            )
            self.relationships.append(r)

    def __run_query(self, query: str) -> pd.DataFrame:
        if not isinstance(query, str):
            raise ValueError(f"Query must be of string type, not {type(query)}")
        if DBConnector.system_to_API[self.system_name] == "ConnectorX":
            return cx.read_sql(self.connection_string, query)
