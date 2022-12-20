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

        self.relationships = []
        self.tables = []
        self.dataframes = dict()

        if system_name in ["mysql", "postgresql"]:
            inputs = [user, host, port, database]
            error_msg = "Please provide non-None values for the user, host, port, and database arguments"
        elif system_name == "snowflake":
            inputs = [user, password, account, database, schema]
            error_msg = "Please provide non-None values for the user, password, account, database, and schema arguments"
        else:
            raise NotImplementedError(
                f"DBConnector does not currently support {database}",
            )

        if None in inputs:
            raise ValueError(error_msg)

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

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        return self.connector.get_primary_key_from_table(table)

    def populate_dataframes(
        self,
        select_only: List[str] = None,
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
