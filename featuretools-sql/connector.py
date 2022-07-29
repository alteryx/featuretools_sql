from collections import namedtuple
import pandas as pd
from db_connectors import mysql_connector, postgres_connector
from typing import List 

class DBConnector:
    Relationship = namedtuple(
        "Relationship",
        ["referenced_table_name", "referenced_column_name", "table_name", "col_name"],
    )

    system_to_API = {"postgresql": "psycopg2", "mysql": "ConnectorX"}
    supported_systems = ["postgresql", "mysql"]

    def __init__(
        self,
        system_name: str,
        user: str,
        password: str,
        host: str,
        port: str,
        database: str,
        schema=None,
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
        self.relationships = []
        self.tables = []
        self.dataframes = dict()
        if system_name == "postgresql":
            if self.schema is None: 
                raise ValueError("Cannot pass None to schema parameter if using Postgres")
            self.connector = postgres_connector(
                host, port, database, user, password, schema
            )
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


    """
    TODO: 

    # def learn_table_schema(self, table: str) -> pd.DataFrame:
    #     schema = self.database
    #     if self.system_name == "mysql":
    #         self.__run_query(
    #             f"SELECT COLUMN_NAME AS `Field`, COLUMN_TYPE AS `Type`, IS_NULLABLE AS `NULL`,  COLUMN_KEY AS `Key`, COLUMN_DEFAULT AS `Default`, EXTRA AS `Extra` FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}';"
    #         )
    """ 

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        return self.connector.get_primary_key_from_table(table)

    def populate_dataframes(self, debug=False) -> dict[str, tuple[pd.DataFrame, str]]:
        self.dataframes = self.connector.populate_dataframes(debug)
        return self.dataframes

    def populate_relationships(self, debug=False) -> List[tuple[str, str, str, str]]:
        self.relationships = self.connector.populate_relationships(debug)
        return self.relationships

