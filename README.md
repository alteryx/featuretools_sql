<p align="center">
<i>Seamlessly integrate SQL data with Featuretools</i>
</p>

# featuretools_sql 
The `featuretools_sql` library allows users to directly import and convert their relational data into a 
[Featuretools](https://github.com/Featuretools/featuretools) compatible format. 

## Installation 
### `featuretools_sql` can be installed with `pip` or `conda`
### Install with `pip` 
`python -m pip install featuretools[sql]`
### Or from the `Conda-forge` channel on [conda](https://anaconda.org/conda-forge/featuretools) 
conda install -c conda-forge featuretools featuretools_sql

## Connecting your database to `featuretools_sql` 
Simply pass in the database connection information. For example:

```python
from connector import DBConnector
import featuretools as ft 

config = dict()
config["system_name"] = "mysql"
config["host"] = "127.0.0.1:3306"
config["password"] = "password"
config["user"] = "root"
config["database"] = "db"

sql_connector = DBConnector(**config) 
entity_set = sql_connector.get_entity_set()

# The entity_set object will have the `relationships` and `dataframes` 
# data structures already populated as member data.

# This means that you are ready to call DFS!
feature_defs, feature_matrix = ft.dfs(dataframes=entity_set.dataframes, relationships=entity_set.relationships)

# If you'd rather inspect the data structures first, you can do that too. 
dataframes = entity_set.dataframes 
relationships = entity_set.relationships 
```

`featuretools_sql` currently supports importing data from the following database management systems: 
  - `MySQL` 
  - `Postgres`

## Testing and Development 


## Support 
The Alteryx community is happy to provide support to users of `Featuretools-SQL`.
Please feel free to file a [GitHub issue](https://github.com/alteryx/featuretools_sql/issues) if you have any questions, encountered any bugs, or
would like to make a feature request! We would love to hear from you.


## Built at Alteryx
`featuretools_sql` is an open source project maintained by Alteryx. To see the other open source projects we’re working on, visit Alteryx Open Source. If building impactful data science pipelines is important to you or your business, please get in touch.

<p align="center">
  <a href="https://www.alteryx.com/open-source">
    <img src="https://alteryx-oss-web-images.s3.amazonaws.com/OpenSource_Logo-01.png" alt="Alteryx Open Source" width="800"/>
  </a>
</p>

