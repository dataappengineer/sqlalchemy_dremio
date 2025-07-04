# -*- coding: utf-8 -*-
"""
Unit tests for SQLAlchemy Dremio dialect changes.
These tests don't require a live Dremio connection.
"""
import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy import create_engine, schema, types
from sqlalchemy.engine import url
from sqlalchemy_dremio.flight import (
    DremioDialect_flight, 
    DremioCompiler, 
    _type_map,
    DremioIdentifierPreparer
)


class TestTypeMapping:
    """Test the enhanced type mapping system."""
    
    def test_expanded_type_map_coverage(self):
        """Test that the type map includes both uppercase and lowercase variants."""
        # Test boolean types
        assert 'boolean' in _type_map
        assert 'BOOLEAN' in _type_map
        assert _type_map['boolean'] == types.BOOLEAN
        assert _type_map['BOOLEAN'] == types.BOOLEAN
        
        # Test binary types
        assert 'varbinary' in _type_map
        assert 'VARBINARY' in _type_map
        assert _type_map['varbinary'] == types.LargeBinary
        assert _type_map['VARBINARY'] == types.LargeBinary
        
        # Test integer types
        assert 'int' in _type_map
        assert 'INT' in _type_map
        assert 'integer' in _type_map
        assert 'INTEGER' in _type_map
        assert 'bigint' in _type_map
        assert 'BIGINT' in _type_map
        assert 'smallint' in _type_map
        
        # Test varchar types
        assert 'varchar' in _type_map
        assert 'VARCHAR' in _type_map
        assert _type_map['varchar'] == types.VARCHAR
        assert _type_map['VARCHAR'] == types.VARCHAR
    
    def test_binary_varying_mapping(self):
        """Test that BINARY VARYING is properly mapped."""
        assert "BINARY VARYING" in _type_map
        assert _type_map["BINARY VARYING"] == types.VARBINARY
    
    def test_smallint_support(self):
        """Test that SMALLINT type is supported."""
        assert 'smallint' in _type_map
        assert _type_map['smallint'] == types.SMALLINT


class TestDialectProperties:
    """Test dialect class properties and methods."""
    
    def test_supports_statement_cache_removed(self):
        """Test that supports_statement_cache property is not set."""
        dialect = DremioDialect_flight()
        # Should not have supports_statement_cache attribute or it should be None/True (default)
        supports_cache = getattr(dialect, 'supports_statement_cache', None)
        # If the attribute exists, it should not be False (the old deprecated value)
        assert supports_cache is not False
    
    def test_dbapi_method_exists(self):
        """Test that dbapi method exists for backward compatibility."""
        dialect = DremioDialect_flight()
        assert hasattr(dialect, 'dbapi')
        assert callable(dialect.dbapi)
    
    def test_import_dbapi_method_removed(self):
        """Test that import_dbapi method is removed."""
        dialect = DremioDialect_flight()
        assert not hasattr(dialect, 'import_dbapi')
    
    def test_do_execute_method_removed(self):
        """Test that do_execute method is removed."""
        dialect = DremioDialect_flight()
        assert not hasattr(dialect, 'do_execute')


class TestTableQuoting:
    """Test table name quoting behavior."""
    
    def test_visit_table_with_schema(self):
        """Test table quoting when schema is provided."""
        compiler = DremioCompiler(DremioDialect_flight())
        
        # Mock table with schema
        table_mock = Mock()
        table_mock.schema = "test_schema"
        table_mock.name = "test_table"
        
        result = compiler.visit_table(table_mock, asfrom=True)
        expected = '"test_schema"."test_table"'
        assert result == expected
    
    def test_visit_table_without_schema(self):
        """Test table quoting when no schema is provided."""
        compiler = DremioCompiler(DremioDialect_flight())
        
        # Mock table without schema
        table_mock = Mock()
        table_mock.schema = None
        table_mock.name = "test_table"
        
        result = compiler.visit_table(table_mock, asfrom=True)
        expected = '"test_table"'
        assert result == expected
    
    def test_visit_table_empty_schema(self):
        """Test table quoting when schema is empty string."""
        compiler = DremioCompiler(DremioDialect_flight())
        
        # Mock table with empty schema
        table_mock = Mock()
        table_mock.schema = ""
        table_mock.name = "test_table"
        
        result = compiler.visit_table(table_mock, asfrom=True)
        expected = '"test_table"'
        assert result == expected
    
    def test_visit_table_complex_schema(self):
        """Test table quoting with complex schema path."""
        compiler = DremioCompiler(DremioDialect_flight())
        
        # Mock table with multi-part schema
        table_mock = Mock()
        table_mock.schema = "space.folder.subfolder"
        table_mock.name = "test_table"
        
        result = compiler.visit_table(table_mock, asfrom=True)
        expected = '"space"."folder"."subfolder"."test_table"'
        assert result == expected


class TestConnectionArgs:
    """Test connection argument creation."""
    
    def test_create_connect_args_basic(self):
        """Test basic connection argument creation."""
        dialect = DremioDialect_flight()
        
        # Create a mock URL
        test_url = url.make_url("dremio+flight://user:pass@localhost:32010/dremio")
        
        args, connect_args = dialect.create_connect_args(test_url)
        
        # Should return connection string and empty connect_args dict
        assert len(args) == 1
        assert isinstance(args[0], str)
        assert isinstance(connect_args, dict)
        
        # Check that basic connection parameters are included
        conn_string = args[0]
        assert "HOST=localhost" in conn_string
        assert "PORT=32010" in conn_string
        assert "UID=user" in conn_string
        assert "PWD=pass" in conn_string
        assert "Schema=dremio" in conn_string
    
    def test_create_connect_args_with_options(self):
        """Test connection argument creation with additional options."""
        dialect = DremioDialect_flight()
        
        # Create URL with query parameters
        test_url = url.make_url(
            "dremio+flight://user:pass@localhost:32010/dremio"
            "?UseEncryption=true&DisableCertificateVerification=false&Token=abc123"
        )
        
        args, connect_args = dialect.create_connect_args(test_url)
        conn_string = args[0]
        
        # Check that additional options are included
        assert "UseEncryption=true" in conn_string
        assert "DisableCertificateVerification=false" in conn_string
        assert "Token=abc123" in conn_string


class TestSQLGeneration:
    """Test SQL query generation improvements."""
    
    def test_sql_without_comments(self):
        """Test that generated SQL doesn't include comment annotations."""
        dialect = DremioDialect_flight()
        
        # Mock connection
        connection_mock = Mock()
        cursor_mock = Mock()
        cursor_mock.__iter__ = Mock(return_value=iter([]))
        connection_mock.execute.return_value = cursor_mock
        
        # Test get_columns - should not include SQL comments
        try:
            dialect.get_columns(connection_mock, "test_table", "test_schema")
        except KeyError:
            # Expected since we're not providing real column data
            pass
        
        # Verify the SQL executed doesn't contain comments
        executed_sql = connection_mock.execute.call_args[0][0]
        assert "/* sqlalchemy:get_columns */" not in executed_sql
        assert executed_sql == 'DESCRIBE "test_schema"."test_table"'


if __name__ == "__main__":
    pytest.main([__file__])
