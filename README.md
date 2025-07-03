# SQLAlchemy Dremio


![PyPI](https://img.shields.io/pypi/v/sqlalchemy_dremio.svg)
![Build](https://github.com/narendrans/sqlalchemy_dremio/workflows/Build/badge.svg)

A SQLAlchemy dialect for Dremio via an Arrow Flight interface.

<!--ts-->
   * [Installation](#installation)
   * [Usage](#usage)
   * [Testing](#testing)
   * [Superset Integration](#superset-integration)
<!--te-->

Installation
------------

From pip:
-----------

`pip install sqlalchemy_dremio`

Or from conda:
--------------
`conda install sqlalchemy-dremio`

To install from source:
`python setup.py install`

Usage
-----

Connection String example:

Dremio Software:

`dremio+flight://user:password@host:port/dremio`

Dremio Cloud:

`dremio+flight://data.dremio.cloud:443/?Token=<your_PAT>`

See [here](https://docs.dremio.com/cloud/security/authentication/personal-access-token/#creating-a-pat) for how to generate a PAT. Make sure your PAT is URL Encoded.

Options:

Schema - (Optional) The schema to use

TLS:

UseEncryption=true|false - (Optional) Enables TLS connection. If you are using Dremio Software, then encryption must be enabled on the Arrow Flight port the Dremio server to use it. 
DisableCertificateVerification=true|false - (Optional) Disables certificate verirication.

WLM:

https://docs.dremio.com/software/advanced-administration/workload-management/#query-tagging--direct-routing-configuration

routing_queue - (Optional) The queue in which queries should run
routing_tag - (Optonal) Routing tag to use.
routing_engine - (Optional) The engine in which the queries should run

Superset Integration
-------------

The ODBC connection to superset is now deprecated. Please update sqlalchemy_dremio to 3.0.2 to use the flight connection.

Release Notes
-------------

3.0.5
-----
- **Enhanced Type Mapping System**: Expanded `_type_map` with comprehensive type mappings supporting both uppercase and lowercase variants for better compatibility
- **Improved Data Type Support**: Added support for `LargeBinary` type for varbinary/VARBINARY data types and `SMALLINT` type mapping
- **SQLAlchemy Compatibility Improvements**: Removed deprecated `supports_statement_cache` property and `import_dbapi` method for better SQLAlchemy 2.x compatibility  
- **Enhanced Table Quoting**: Updated `visit_table` method to consistently quote table names when no schema is provided, ensuring proper SQL generation
- **Streamlined SQL Execution**: 
  - Removed SQL comment annotations (e.g., `/* sqlalchemy:get_columns */`) for cleaner query generation
  - Removed `text()` wrapper from SQL execution calls for simplified execution
  - Simplified `get_schema_names` method to directly execute "SHOW SCHEMAS"
- **Improved Schema Handling**: Updated `get_table_names` method with cleaner conditional logic for schema filtering
- **Removed Legacy Workarounds**: Eliminated the `do_execute` method that handled parameterized statement workarounds, relying on native SQLAlchemy handling
- **Code Quality**: Added `import re` for future regex functionality and improved overall code organization

3.0.4
-----
- Updates type mappings, added support for SQLAlchemy 2 & workaround for parameterized statements for flight

3.0.3
-----
- Add back missing routing_engine property.

3.0.2
-----
- Add implementations of has_table and get_view_names.

3.0.1
-----
- Made connection string property keys case-insensitive
- Fix incorrect lookup of the token property
- Fix incorrect lookup of the DisableCertificateVerification property
