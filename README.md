<p align="center">
<img width=50% src="https://www.featuretools.com/wp-content/uploads/2017/12/FeatureLabs-Logo-Tangerine-800.png" alt="Featuretool-SQL" />
</p>
<p align="center">
<i>"EntitySet relationships made easy!</a>
</p>

<p align="center">
    <a href="https://github.com/alteryx/featuretools/actions?query=branch%3Amain+workflow%3ATests" target="_blank">
        <img src="https://github.com/alteryx/featuretools/workflows/Tests/badge.svg?branch=main" alt="Tests" />
    </a>
    <a href="https://codecov.io/gh/alteryx/featuretools">
        <img src="https://codecov.io/gh/alteryx/featuretools/branch/main/graph/badge.svg"/>
    </a>
    <a href='https://featuretools.alteryx.com/en/stable/?badge=stable'>
        <img src='https://readthedocs.com/projects/feature-labs-inc-featuretools/badge/?version=stable' alt='Documentation Status' />
    </a>
    <a href="https://badge.fury.io/py/featuretools" target="_blank">
        <img src="https://badge.fury.io/py/featuretools.svg?maxAge=2592000" alt="PyPI Version" />
    </a>
    <a href="https://anaconda.org/conda-forge/featuretools" target="_blank">
        <img src="https://anaconda.org/conda-forge/featuretools/badges/version.svg" alt="Anaconda Version" />
    </a>
    <a href="https://stackoverflow.com/questions/tagged/featuretools" target="_blank">
        <img src="http://img.shields.io/badge/questions-on_stackoverflow-blue.svg" alt="StackOverflow" />
    </a>
    <a href="https://pepy.tech/project/featuretools" target="_blank">
        <img src="https://pepy.tech/badge/featuretools/month" alt="PyPI Downloads" />
    </a>
</p>
<hr>

# featuretools_sql 
The `featuretools_sql` library allows users to directly import and convert their relational data into a 
[Featuretools](https://github.com/Featuretools/featuretools) compatible format. 

## Installation 
TODO 

## Docker

```
docker compose up
```

### Run Webclient

Go to http://localhost:8090/

To login to postgres:

server: postgres
username: postgres
password: example

To login to mysql:

server: mysql
username: root
password: example

## Connecting your database to `featuretools_sql` 
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

`featuretools_sql` currently supports importing data from the following database management systems: 
  - `MySQL` 

## Development
TODO

## Built at Alteryx
`featuretools_sql` is an open source project maintained by Alteryx. To see the other open source projects we’re working on, visit Alteryx Open Source. If building impactful data science pipelines is important to you or your business, please get in touch.

<p align="center">
  <a href="https://www.alteryx.com/open-source">
    <img src="https://alteryx-oss-web-images.s3.amazonaws.com/OpenSource_Logo-01.png" alt="Alteryx Open Source" width="800"/>
  </a>
</p>
