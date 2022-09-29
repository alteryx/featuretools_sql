from collections import namedtuple
from typing import Dict, List, Optional, Tuple

import pandas as pd

from featuretools_sql.db_connectors import (
    MySQLConnector,
    PostgresConnector,
    SnowflakeConnector,
)


class DBConnector:
    Relationship = namedtuple(
        "Relationship",
        ["referenced_table_name", "referenced_column_name", "table_name", "col_name"],
    )

    supported_systems = ["postgresql", "mysql", "snowflake"]

    def __init__(
        self,
        system_name: str,
        user: str,
        database: str,
        account: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        password: Optional[str] = None,
        schema=None,
    ):
        self.system_name = system_name
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.schema = schema

        if system_name not in DBConnector.supported_systems:
            raise NotImplementedError(
                f"DBConnector does not currently support {database}",
            )
        self.relationships = []
        self.tables = []
        self.dataframes = dict()

        if system_name in ["postgresql", "mysql"]:
            if None in [user, host, port, database]:
                raise ValueError("Cannot pass None as argument to DBConnector constructor")

        if system_name == "snowflake":
            if None in [user, password, account, database, schema]:
                raise ValueError("Must pass in values for user, password, account, and database that are not None")

        if system_name == "postgresql":
            self.connector = PostgresConnector(
                host,
                port,
                database,
                user,
                password,
                schema,
            )
        elif system_name == "mysql":
            self.connector = MySQLConnector(host, port, database, user, password)
        elif system_name == "snowflake":
            self.connector = SnowflakeConnector(user, password, account, database, schema)

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

    def populate_dataframes(
        self,
        select_only=None,
    ) -> Dict[str, Tuple[pd.DataFrame, str]]:
        self.dataframes = self.connector.populate_dataframes(select_only)
        return self.dataframes

    def populate_relationships(
        self,
    ) -> List[Tuple[str, str, str, str]]:
        self.relationships = self.connector.populate_relationships()
        return self.relationships

    def get_entityset(self):
        return self.connector.get_entityset()
