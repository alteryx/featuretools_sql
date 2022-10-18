from typing import Dict, List, Tuple

import pandas as pd
import pandas.io.sql as sqlio
from featuretools import EntitySet
from sqlalchemy import create_engine


class PostgresConnector:
    def __init__(self, host, port, database, user, password, schema):

        if password:
            self.engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
        else:
            self.engine = create_engine(f"postgresql://{user}@{host}:{port}/{database}")

        self.system_name = "postgresql"
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.schema = schema
        self.tables = []

    def all_tables(self, select_only=None) -> pd.DataFrame:
        if isinstance(select_only, list):
            select_only_tables = ", ".join([f"'{i}'" for i in select_only])
            return self.run_query(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.schema}' AND TABLE_NAME IN ({select_only_tables});",
            )
        elif select_only is None:
            return self.run_query(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.schema}';",
            )
        else:
            raise ValueError(
                f"select_only parameter must be list or None, got {type(select_only)}",
            )

    def populate_dataframes(
        self,
        select_only=None,
    ) -> Dict[str, Tuple[pd.DataFrame, str]]:
        tables_df = self.all_tables(select_only)
        table_index = "table_name"
        self.tables = []
        dataframes = dict()
        for table in tables_df[table_index].values:
            self.tables.append(table)
            table_df = self.get_table(table)
            table_key = self.get_primary_key_from_table(table).values[0]
            dataframes[table] = (table_df, table_key)
        return dataframes

    def get_table(self, table: str) -> pd.DataFrame:
        return self.run_query(f"SELECT * FROM {table}")

    def populate_relationships(self) -> List[Tuple[str, str, str, str]]:
        query_str = """
            select kcu.table_schema || '.' || kcu.table_name as foreign_table,
            rel_kcu.table_schema || '.' || rel_kcu.table_name as primary_table,
            kcu.column_name as fk_column,
            rel_kcu.column_name as pk_column
            from information_schema.table_constraints tco
            join information_schema.key_column_usage kcu
            on tco.constraint_schema = kcu.constraint_schema
            and tco.constraint_name = kcu.constraint_name
            join information_schema.referential_constraints rco
            on tco.constraint_schema = rco.constraint_schema
            and tco.constraint_name = rco.constraint_name
            join information_schema.key_column_usage rel_kcu
            on rco.unique_constraint_schema = rel_kcu.constraint_schema
            and rco.unique_constraint_name = rel_kcu.constraint_name
            and kcu.ordinal_position = rel_kcu.ordinal_position
            where tco.constraint_type = 'FOREIGN KEY'
            order by kcu.table_schema,
            kcu.table_name,
            kcu.ordinal_position;
            """
        relationships = []
        foreign_keys = self.run_query(query_str)
        if self.system_name == "postgresql":
            for (
                foreign_table,
                primary_table,
                foreign_col,
                primary_col,
            ) in foreign_keys.values:
                if "." in foreign_table:
                    foreign_table = self.__cut_schema_name(foreign_table)
                if "." in primary_table:
                    primary_table = self.__cut_schema_name(primary_table)
                if foreign_table in self.tables and primary_table in self.tables:
                    relationships.append((primary_table, primary_col, foreign_table, foreign_col))
        return relationships

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        df = self.run_query(
            f"SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type FROM pg_index i JOIN   pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) WHERE  i.indrelid = '{table}'::regclass AND i.indisprimary;",
        )
        if df.empty:
            raise ValueError(
                f"In order to determine table relationships, each table needs to have a primary key. Currently, {table} does not have a defined primary key. Please define one and retry.",
            )
        return df["attname"]

    def __cut_schema_name(self, string: str) -> str:
        return string[string.find(".") + 1 :]

    def run_query(self, query: str) -> pd.DataFrame:
        return sqlio.read_sql_query(query, self.engine)

    def get_entityset(self) -> EntitySet:
        dataframes = self.populate_dataframes()
        relationships = self.populate_relationships()
        return EntitySet(dataframes=dataframes, relationships=relationships)
