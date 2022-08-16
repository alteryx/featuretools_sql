def verify_relationships_are_equal(actual, expected):
    for r, es_rel in zip(actual, expected):
        parent_table, parent_col, child_table, child_col = r
        assert child_table == es_rel._child_dataframe_name
        assert parent_table == es_rel._parent_dataframe_name
        assert child_col == es_rel._child_column_name
        assert parent_col == es_rel._parent_column_name


def add_foreign_key_postgres(
    connection,
    referencing_table,
    constraint_name,
    referencing_col,
    referenced_table,
    referenced_col,
):
    connection.execute(
        f"ALTER TABLE {referencing_table} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({referencing_col}) REFERENCES {referenced_table} ({referenced_col}) MATCH FULL"
    )


def load_dataframes_into_engine(dataframes, engine):
    """
    Given an entityset and an engine,
    load all the dataframes in the entity set into
    the relational database. Also, set the primary keys
    """
    for df in dataframes:
        name = df.ww.name
        idx_col = df.ww.index

        df.to_sql(name, engine, index=False)

        with engine.connect() as con:
            con.execute(f"ALTER TABLE public.{name} add primary key ({idx_col})")
