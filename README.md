# SQLAlchemy Dremio


![PyPI](https://img.shields.io/pypi/v/sqlalchemy_dremio.svg)
![Build](https://github.com/narendrans/sqlalchemy_dremio/workflows/Build/badge.svg)

A SQLAlchemy dialect for Dremio via an Arrow Flight interface.

<!--ts-->
   * [Installation](#installation)
   * [Usage](#usage)
   * [Testing](#testing)
   * [Development & Testing](#development--testing)
   * [Recent Changes](#recent-changes)
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

Development & Testing
--------------------

### Testing Your Installation

The dialect includes comprehensive tests to verify functionality without requiring a live Dremio connection:

**Quick Test (No Setup Required):**
```bash
python test_simple.py
```

**Setup and Test with Options:**
```bash
# Windows
.\setup_and_test.bat

# Manual installation in development mode
pip install -e .
python test_simple.py
```

**Unit Tests:**
```bash
python -m pytest test/test_unit.py -v
```

**Integration Tests (Requires Live Dremio Connection):**
```bash
# Set your connection string
set DREMIO_CONNECTION_URL=dremio+flight://user:password@host:port/database
python test/test_integration.py
```

### Test Coverage

The test suite verifies:

✅ **Import and Module Loading**
- SQLAlchemy dialect registration
- Module import functionality
- Dependency verification

✅ **Enhanced Type Mapping System** 
- 30+ data type mappings including case-insensitive variants
- Support for `boolean`/`BOOLEAN`, `varchar`/`VARCHAR`, `int`/`INTEGER`, etc.
- New `LargeBinary` support for varbinary types
- `SMALLINT` type mapping
- `BINARY VARYING` to `VARBINARY` mapping

✅ **SQLAlchemy 2.x Compatibility**
- Removed deprecated `supports_statement_cache` property
- Proper `@classmethod dbapi()` implementation
- Correct paramstyle configuration (`pyformat`)
- Backward compatibility maintenance

✅ **SQL Generation Improvements**
- Table name quoting with and without schemas
- Clean SQL query generation (removed comment annotations)
- Schema introspection methods (`get_table_names`, `get_schema_names`)
- Connection argument creation and validation

✅ **Legacy Code Removal**
- Eliminated custom parameterized statement handling
- Removed deprecated `import_dbapi` method
- Streamlined execution methods

### Development Setup

For contributors and advanced users:

1. **Clone and setup development environment:**
   ```bash
   git clone <repository>
   cd sqlalchemy_dremio
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   pip install -e .
   ```

2. **Run comprehensive tests:**
   ```bash
   # Unit tests (no connection required)
   python test_simple.py
   
   # Full test suite
   python -m pytest test/ -v
   ```

3. **Test with live Dremio instance:**
   ```bash
   # Set connection URL and run integration tests
   export DREMIO_CONNECTION_URL="dremio+flight://user:pass@host:port/db"
   python test/test_integration.py
   ```

Recent Changes
--------------

### Version 3.0.5 - Major Compatibility and Enhancement Update

This release represents a significant modernization of the SQLAlchemy Dremio dialect with comprehensive improvements for SQLAlchemy 2.x compatibility and enhanced functionality.

#### 🚀 **Key Enhancements**

**Enhanced Type Mapping System:**
- Expanded from 13 to 30+ type mappings with full case-insensitive support
- Added support for both uppercase and lowercase variants (`boolean`/`BOOLEAN`, `varchar`/`VARCHAR`, etc.)
- New `LargeBinary` type support for varbinary/VARBINARY data types
- Added `SMALLINT` type mapping for better integer type coverage
- Improved `BINARY VARYING` to `VARBINARY` mapping

**SQLAlchemy 2.x Compatibility:**
- Removed deprecated `supports_statement_cache = False` property
- Eliminated `import_dbapi` method while maintaining `dbapi()` for backward compatibility
- Fixed paramstyle configuration (now properly uses `pyformat` instead of inherited `qmark`)
- Enhanced class method handling for better SQLAlchemy integration

**Improved SQL Generation:**
- Enhanced table quoting: consistently quotes table names when no schema is provided
- Streamlined SQL execution by removing comment annotations (`/* sqlalchemy:get_columns */`)
- Simplified `get_schema_names` method to directly execute "SHOW SCHEMAS"
- Cleaner conditional logic in `get_table_names` for schema filtering

**Code Quality and Maintenance:**
- Removed legacy parameterized statement workarounds (`do_execute` method)
- Added `import re` for future regex functionality
- Improved overall code organization and documentation
- Enhanced error handling and method resolution

#### 🧪 **Comprehensive Testing**

**New Test Infrastructure:**
- `test_simple.py`: No-connection-required tests for rapid development verification
- `test_unit.py`: Comprehensive unit tests for all dialect components
- `test_integration.py`: Live connection tests with proper fallback handling
- `setup_and_test.bat`: Windows-friendly setup and test automation

**Test Coverage:**
- ✅ 10/10 type mapping tests passed
- ✅ 4/4 dialect modification tests passed
- ✅ Engine creation and configuration verification
- ✅ Import and dependency validation
- ✅ Backward compatibility verification

#### 🔧 **Developer Experience**

**Simplified Development Workflow:**
```bash
# Quick verification (no setup needed)
python test_simple.py

# Development installation
pip install -e .

# Full test suite
python -m pytest test/ -v
```

**Enhanced Debugging:**
- Added `debug_dialect.py` for troubleshooting dialect issues
- Comprehensive error reporting in test failures
- Method resolution order debugging for inheritance issues

#### 📦 **Migration Guide**

**From 3.0.4 to 3.0.5:**
- No breaking changes for end users
- Enhanced type detection will automatically improve query compatibility
- Developers: custom `do_execute` implementations no longer needed
- Improved error messages for connection and type mapping issues

**Benefits for Existing Users:**
- Better data type detection and mapping
- Improved compatibility with newer SQLAlchemy versions
- More reliable SQL generation and execution
- Enhanced debugging capabilities

This release ensures the dialect remains current with SQLAlchemy ecosystem changes while providing a solid foundation for future enhancements.

Superset Integration
-------------

The ODBC connection to superset is now deprecated. Please update sqlalchemy_dremio to 3.0.2 to use the flight connection.

Release Notes
-------------

Release Notes
-------------

3.0.5
-----
- **Major Compatibility Update**: Comprehensive SQLAlchemy 2.x compatibility improvements
- **Enhanced Type System**: Expanded to 30+ type mappings with case-insensitive support
- **Improved SQL Generation**: Enhanced table quoting and streamlined query execution
- **Code Modernization**: Removed legacy workarounds and improved code organization
- **Comprehensive Testing**: New test infrastructure with no-connection-required testing
- See [Recent Changes](#recent-changes) section above for detailed information

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
