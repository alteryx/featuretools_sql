from typing import Dict, List, Tuple

import pandas as pd
import pandas.io.sql as sqlio
from featuretools import EntitySet
from sqlalchemy import create_engine


class SnowflakeConnector:
    def __init__(self, user, password, account, database, schema):
        self.system_name = "snowflake"
        self.user = user
        self.password = password
        self.account = account
        self.database = database
        self.schema = schema
        self.engine = create_engine(f'snowflake://{user}:{password}@{account}')
        self.tables = []

    def all_tables(self, select_only=None) -> pd.DataFrame:
        if isinstance(select_only, list):
            select_only_tables = ", ".join([f"'{i}'" for i in select_only])
            return self.run_query(
                f"SELECT TABLE_NAME FROM {self.database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.schema}' AND TABLE_NAME IN ({select_only_tables});",
            )
        elif select_only is None:
            return self.run_query(
                f"SELECT TABLE_NAME FROM {self.database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.schema}';",
            )
        else:
            raise ValueError(
                f"select_only parameter must be list or None, got {type(select_only)}",
            )

    def _is_mixed_case(self, name: str):
        return not name.islower() and not name.isupper()

    def populate_dataframes(
        self,
        select_only=None,
    ) -> Dict[str, Tuple[pd.DataFrame, str]]:
        tables_df = self.all_tables(select_only)
        table_index = "table_name"
        dataframes = dict()
        for table in tables_df[table_index].values:
            self.tables.append(table)
            table_df = self.get_table(table)
            table_key = self.get_primary_key_from_table(table).values[0]
            if not self._is_mixed_case(table_key):
                table_key = table_key.lower()
            dataframes[table] = (table_df, table_key)
        return dataframes

    def get_table(self, table: str) -> pd.DataFrame:
        return self.run_query(f"SELECT * FROM {self.database}.{self.schema}.{table}")

    def populate_relationships(self) -> List[Tuple[str, str, str, str]]:
        relationships = []
        foreign_keys = self.run_query("SHOW IMPORTED KEYS;")
        for (
            _, _, _,
            primary_table,
            primary_col,
            _, _,
            foreign_table,
            foreign_col,
            _, _, _, _, _, _, _, _
        ) in foreign_keys.values:
            if "." in foreign_table:
                foreign_table = self.__cut_schema_name(foreign_table)
            if "." in primary_table:
                primary_table = self.__cut_schema_name(primary_table)
            if not self._is_mixed_case(primary_col):
                primary_col = primary_col.lower()
            if not self._is_mixed_case(foreign_col):
                foreign_col = foreign_col.lower()
            if foreign_table in self.tables and primary_table in self.tables:
                r = (primary_table, primary_col, foreign_table, foreign_col)
                relationships.append(r)
        return relationships

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        df = self.run_query(
            f"SHOW PRIMARY KEYS IN {self.database}.{self.schema}.{table}",
        )
        if df.empty:
            raise ValueError(
                f"In order to determine table relationships, each table needs to have a primary key. Currently, {table} does not have a defined primary key. Please define one and retry.",
            )
        return df["column_name"]

    def __cut_schema_name(self, string: str) -> str:
        return string[string.find(".") + 1 :]

    def run_query(self, query: str) -> pd.DataFrame:
        return sqlio.read_sql_query(query, self.engine)

    def get_entityset(self) -> EntitySet:
        dataframes = self.populate_dataframes()
        relationships = self.populate_relationships()
        return EntitySet(dataframes=dataframes, relationships=relationships)
