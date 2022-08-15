#from typing import List
import pandas as pd
import pandas.io.sql as sqlio
import psycopg2

from featuretools import EntitySet

class PostgresConnector:
    def __init__(self, host, port, database, user, password, schema):

        conn_dict = {}
        conn_dict["host"] = host
        conn_dict["port"] = port
        conn_dict["database"] = database
        conn_dict["user"] = user

        if password:
            conn_dict["password"] = password
       
        self.postgres_connection = psycopg2.connect(**conn_dict)

        self.system_name = "postgresql"
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.schema = schema
        self.tables = []

    def all_tables(self) -> pd.DataFrame:
        return self.run_query(
            f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.schema}';"
        )

    def populate_dataframes(self, debug=False): # 3.9 and above -> dict[str, tuple[pd.DataFrame, str]]:
        tables_df = self.all_tables()
        table_index = "table_name"
        self.tables = []
        dataframes = dict()
        for table in tables_df[table_index].values:
            self.tables.append(table)
            table_df = self.get_table(table)
            # TODO: error handling on tables here

            table_key = self.get_primary_key_from_table(table).values[0]
            dataframes[table] = (table_df, table_key)
        if debug:
            for k, v in self.dataframes.items():
                print(f"Name: {k}")
                print(f"df: {v}")
                print()
        return dataframes

    def get_table(self, table: str) -> pd.DataFrame:
        return self.run_query(f"SELECT * FROM {table}")

    def populate_relationships(self, debug=False): # 3.9 and above -> List[tuple(str, str, str, str)]
        query_str = (
            """
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
        )
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
                r = (primary_table, primary_col, foreign_table, foreign_col)
                relationships.append(r)
        if debug: 
            for referenced_table_name, referenced_column_name, table_name, col_name in self.relationships:
                print(f"referenced_table_name: {referenced_table_name}")
                print(f"referenced_column_name: {referenced_column_name}")
                print(f"table_name: {table_name}")
                print(f"col_name: {col_name}")
        return relationships

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        df = self.run_query(
            f"SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type FROM pg_index i JOIN   pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) WHERE  i.indrelid = '{table}'::regclass AND i.indisprimary;"
        )
        return df["attname"]

    def __cut_schema_name(self, string: str) -> str:
        return string[string.find(".") + 1 :]

    def run_query(self, query: str) -> pd.DataFrame:
        return sqlio.read_sql_query(query, self.postgres_connection)

    def get_entity_set(self): 
        dataframes = self.populate_dataframes()
        relationships = self.populate_relationships()
        return EntitySet(dataframes=dataframes,relationships=relationships)