# featuretools-sql 
The `featuretools-sql` library allows users to directly import and convert their relational data into a 
[Featuretools](https://github.com/Featuretools/featuretools) compatible format. 

## Installation 
TODO 

## Connecting your database to `featuretools-sql` 
Simply pass in the database connection information. For example:

```python
from connector import DBConnector

config = dict()
config["system_name"] = "mysql"
config["host"] = "127.0.0.1:3306"
config["password"] = "password"
config["user"] = "root"
config["database"] = "db"

sql_connector = DBConnector(**config) 
entity_set = sql_connector.get_entity_set()
```

The relational data is now a `featuretools.EntitySet` object, ready for feature engineering.

`featuretools-sql` currently supports importing data from the following database management systems: 
  - `MySQL` 

## Development
TODO

## Built at Alteryx
`featuretools-sql` is an open source project maintained by Alteryx. To see the other open source projects we’re working on, visit Alteryx Open Source. If building impactful data science pipelines is important to you or your business, please get in touch.

<p align="center">
  <a href="https://www.alteryx.com/open-source">
    <img src="https://alteryx-oss-web-images.s3.amazonaws.com/OpenSource_Logo-01.png" alt="Alteryx Open Source" width="800"/>
  </a>
</p>
