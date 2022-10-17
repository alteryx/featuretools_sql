from typing import Dict, List, Tuple

import pandas as pd
import pandas.io.sql as sqlio
from featuretools import EntitySet
from sqlalchemy import create_engine


class MySQLConnector:
    def __init__(self, host, port, database, user, password):
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(connection_string)
        self.system_name = "mysql"
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.tables = []
        self.relationships = []

    def all_tables(self, select_only=None) -> pd.DataFrame:
        if isinstance(select_only, list):
            select_only_tables = ", ".join([f"'{i}'" for i in select_only])
            return self.run_query(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME IN ({select_only_tables});",
            )
        elif select_only is None:
            return self.run_query(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database}'",
            )
        else:
            raise ValueError(
                f"select_only parameter must be list or None, got {type(select_only)}",
            )

    def populate_dataframes(
        self,
        select_only=None,
    ) -> Dict[str, Tuple[pd.DataFrame, str]]:
        dataframes = dict()
        tables_df = self.all_tables(select_only)
        table_index = "TABLE_NAME"
        for table in tables_df[table_index].values:
            self.tables.append(table)
            table_df = self.get_table(table)
            table_key = self.get_primary_key_from_table(table).values[0]
            dataframes[table] = (table_df, table_key)
        return dataframes

    def get_table(self, table: str) -> pd.DataFrame:
        return self.run_query(f"SELECT * FROM {table}")

    def populate_relationships(self) -> List[Tuple[str, str, str, str]]:
        query_str = f"SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = '{self.database}'"
        foreign_keys = self.run_query(query_str)
        for (
            table_name,
            col_name,
            referenced_table_name,
            referenced_column_name,
        ) in foreign_keys.values:
            r = (
                referenced_table_name,
                referenced_column_name,
                table_name,
                col_name,
            )
            if referenced_table_name in self.tables and table_name in self.tables:
                self.relationships.append(r)

        return self.relationships

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        df = self.run_query(
            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' AND COLUMN_KEY = 'PRI';",
        )
        if df.empty:
            raise ValueError(
                f"In order to determine table relationships, each table needs to have a primary key. Currently, {table} does not have a defined primary key. Please define one and retry.",
            )
        return df["COLUMN_NAME"]

    def run_query(self, query: str) -> pd.DataFrame:
        return sqlio.read_sql_query(query, self.engine)

    def get_entityset(self) -> EntitySet:
        dataframes = self.populate_dataframes()
        relationships = self.populate_relationships()
        return EntitySet(dataframes=dataframes, relationships=relationships)
