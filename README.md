# Featuretools-SQL 
The `featuretools_sql` library allows you to directly import your relational data into
[Featuretools](https://github.com/alteryx/featuretools) to run automated feature engineering.

<p align="center">
<i>Automated creation of EntitySets from relational data stored in SQL databases</i>
</p>

</a>
    <a href="https://pepy.tech/project/featuretools-sql" target="_blank">
    <img src="https://pepy.tech/badge/featuretools-sql/month" alt="PyPI Downloads" />
</a>

## Installation 

Install with pip:

```shell
python -m pip install "featuretools[sql]"
```

## Example
Simply pass in the database connection information. For example:

```python
from featuretools_sql.connector import DBConnector

sql_connector = DBConnector(
    system_name = "mysql",
    host = "127.0.0.1:3306"
    user = "root",
    password = "password",
    database = "db"
) 
entityset = sql_connector.get_entityset()
```

The `entityset` object will have the `relationships` and `DataFrames` already populated, allowing you to call featuretools.DFS and run automated feature generation.

```python
import featuretools as ft

feature_defs, feature_matrix = ft.dfs(
    entityset=entityset,
    target_entity='target_table_name'
)
```

We currently supports importing data from the following relational database systems: 
  - `MySQL` 
  - `PostgreSQL`
  - `Snowflake`

## Support
The Featuretools community is happy to provide support to users. Project support can be found in four places depending on the type of question:
1. For usage questions, use [Stack Overflow](https://stackoverflow.com/questions/tagged/featuretools) with the `featuretools` tag.
2. For bugs, issues, or feature requests start a [Github issue](https://github.com/alteryx/featuretools_sql/issues).
3. For discussion regarding development, use [Slack](https://join.slack.com/t/alteryx-oss/shared_invite/zt-182tyvuxv-NzIn6eiCEf8TBziuKp0bNA).
4. For everything else, the core developers can be reached by email at open_source_support@alteryx.com

## Built at Alteryx

`featuretools_sql` is an open source project maintained by [Alteryx](https://www.alteryx.com). To see the other open source projects we’re working on, visit [Alteryx Open Source](https://www.alteryx.com/open-source). If building impactful data science pipelines is important to you or your business, please get in touch.

<p align="center">
  <a href="https://www.alteryx.com/open-source">
    <img src="https://alteryx-oss-web-images.s3.amazonaws.com/OpenSource_Logo-01.png" alt="Alteryx Open Source" width="800"/>
  </a>
</p>
