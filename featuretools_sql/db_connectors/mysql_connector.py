import connectorx as cx
import pandas as pd
from featuretools import EntitySet
from typing import Tuple, Dict, List


class MySQLConnector:
    def __init__(self, host, port, database, user, password):
        self.connection_string = f"mysql://{user}:{password}@{host}:{port}/{database}"
        self.system_name = "postgresql"
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.tables = []

        self.dataframes = dict()
        self.relationships = []

    def all_tables(self) -> pd.DataFrame:
        return self.run_query(
            f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.database}';"
        )

    def populate_dataframes(
        self, debug=False
    ) -> Dict[str, Tuple[pd.DataFrame, str]]:
        tables_df = self.all_tables()
        table_index = "TABLE_NAME"
        for table in tables_df[table_index].values:
            self.tables.append(table)
            table_df = self.get_table(table)
            table_key = self.get_primary_key_from_table(table).values[0]
            self.dataframes[table] = (table_df, table_key)
        if debug:
            for k, v in self.dataframes.items():
                print(f"Name: {k}")
                print(f"df: {v}")
                print()
        return self.dataframes

    def get_table(self, table: str) -> pd.DataFrame:
        return self.run_query(f"SELECT * FROM {table}")

    def populate_relationships(
        self, debug=False
    ) -> List[tuple(str, str, str, str)]:
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
            self.relationships.append(r)
        if debug:
            for (
                referenced_table_name,
                referenced_column_name,
                table_name,
                col_name,
            ) in self.relationships:
                print(f"referenced_table_name: {referenced_table_name}")
                print(f"referenced_column_name: {referenced_column_name}")
                print(f"table_name: {table_name}")
                print(f"col_name: {col_name}")

        return self.relationships

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        df = self.run_query(
            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' AND COLUMN_KEY = 'PRI';"
        )
        if df.empty:
            raise ValueError(
                f"In order to determine table relationships, each table needs to have a primary key. Currently, {table} does not have a defined primary key. Please define one and retry."
            )
        return df["COLUMN_NAME"]

    def run_query(self, query: str) -> pd.DataFrame:
        return cx.read_sql(self.connection_string, query)

    def get_entity_set(self):
        dataframes = self.populate_dataframes()
        relationships = self.populate_relationships()
        return EntitySet(dataframes=dataframes, relationships=relationships)
