import psycopg2 
import pandas as pd 
import pandas.io.sql as sqlio 
from typing import List 

class postgres_connector: 

    def __init__(self, host, port, database, user, password, schema): 
        conn_string = "host='{}' port={} dbname='{}' user={} password={}".format(host, port, database, user, password)
        self.postgres_connection = psycopg2.connect(conn_string) 

        self.system_name = "postgresql"
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port 
        self.schema = schema
        self.tables = []

        self.dataframes = dict() 
        self.relationships = [] 


    def all_tables(self) -> pd.DataFrame:
        return self.run_query(
                f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{self.schema}';"
            )

    def populate_dataframes(self,debug=False) :
        tables_df = self.all_tables()
        table_index = "table_name"
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


    def populate_relationships(self) -> List[pd.DataFrame]: 
        query_str = ("select kcu.table_schema || '.' || kcu.table_name as foreign_table, " 
                    "'>-' as rel, " 
                    "rel_kcu.table_schema || '.' || rel_kcu.table_name as primary_table, " 
                    "kcu.ordinal_position as no, " 
                    "kcu.column_name as fk_column, " 
                    "'=' as join, " 
                    "rel_kcu.column_name as pk_column, " 
                    "kcu.constraint_name " 
                    "from information_schema.table_constraints tco " 
                    "join information_schema.key_column_usage kcu " 
                    "on tco.constraint_schema = kcu.constraint_schema " 
                    "and tco.constraint_name = kcu.constraint_name " 
                    "join information_schema.referential_constraints rco " 
                    "on tco.constraint_schema = rco.constraint_schema " 
                    "and tco.constraint_name = rco.constraint_name " 
                    "join information_schema.key_column_usage rel_kcu " 
                    "on rco.unique_constraint_schema = rel_kcu.constraint_schema " 
                    "and rco.unique_constraint_name = rel_kcu.constraint_name " 
                    "and kcu.ordinal_position = rel_kcu.ordinal_position " 
                    "where tco.constraint_type = 'FOREIGN KEY' " 
                    "order by kcu.table_schema, " 
                    "kcu.table_name,  " 
                    "kcu.ordinal_position ;"
        ) 
        foreign_keys = self.run_query(query_str)
        if self.system_name == "postgresql": 
            for (foreign_table, _, primary_table, _, foreign_col, _, primary_col, _) in foreign_keys.values:
                if "." in foreign_table: 
                    foreign_table = self.__cut_schema_name(foreign_table) 
                if "." in primary_table: 
                    primary_table = self.__cut_schema_name(primary_table)
                r = (primary_table, primary_col,foreign_table, foreign_col)
                self.relationships.append(r) 
        return self.relationships

    def get_primary_key_from_table(self, table: str) -> pd.DataFrame:
        df = self.run_query(
            f"SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type FROM pg_index i JOIN   pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) WHERE  i.indrelid = '{table}'::regclass AND i.indisprimary;"
        )
        return df["attname"]

    def __cut_schema_name(self, string : str) -> str: 
        return string[string.find(".")+1:]

    def run_query(self, query: str) -> pd.DataFrame: 
        return sqlio.read_sql_query(query, self.postgres_connection)