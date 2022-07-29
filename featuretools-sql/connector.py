from collections import defaultdict, namedtuple

import connectorx as cx
import pandas as pd
import psycopg2
import pandas.io.sql as sqlio 

from db_connectors import postgres_connector
from db_connectors import mysql_connector
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
        #self.connection_string = f"{system_name}://{user}:{password}@{host}:{port}/{database}"
        self.relationships = []
        self.tables = []
        self.dataframes = dict()
        if system_name == "postgresql": 
            assert schema != None 
            self.connector = postgres_connector(host, port, database, user, password, schema)
        elif system_name == "mysql": 
            self.connector = mysql_connector(host, port, database, user, password)

    def change_system_name(self, system_name: str):
        self.system_name = system_name

    def change_password(self, new_password: str):
        self.password = new_password

    def change_user(self, new_user: str):
        self.new_user = new_user

    def change_host(self, new_host: str):
        self.new_host = new_host

    def all_tables(self) -> pd.DataFrame:
        return self.connector.all_tables()

    # def learn_table_schema(self, table: str) -> pd.DataFrame:
    #     schema = self.database
    #     if self.system_name == "mysql":
    #         self.__run_query(
    #             f"SELECT COLUMN_NAME AS `Field`, COLUMN_TYPE AS `Type`, IS_NULLABLE AS `NULL`,  COLUMN_KEY AS `Key`, COLUMN_DEFAULT AS `Default`, EXTRA AS `Extra` FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}';"
    #         )

    # def get_table(self, table: str) -> pd.DataFrame:
    #     return self.__run_query(f"SELECT * FROM {table}")

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        return self.connector.get_primary_key_from_table(table)

    def populate_dataframes(self, debug=False):
        self.dataframes = self.connector.populate_dataframes(debug)
        return self.dataframes 

    def populate_relationships(self, debug=False):
        self.relationships = self.connector.populate_relationships()
        return self.relationships

    # def __run_query(self, query: str) -> pd.DataFrame:
    #     if not isinstance(query, str):
    #         raise ValueError(f"Query must be of string type, not {type(query)}")
    #     return self.connector.run_query(query) 