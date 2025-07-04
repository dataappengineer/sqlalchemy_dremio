# -*- coding: utf-8 -*-
"""
Integration tests for SQLAlchemy Dremio dialect.
These tests can run with or without a live Dremio connection.
"""
import os
import pytest
from unittest.mock import Mock, patch
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError
import sqlalchemy_dremio


class TestDialectIntegration:
    """Integration tests for the dialect."""
    
    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine for testing without live connection."""
        engine = create_engine("dremio+flight://test:test@localhost:32010/test")
        return engine
    
    def test_dialect_registration(self):
        """Test that the dialect is properly registered."""
        # Test that we can create an engine with the dremio+flight URL
        engine = create_engine("dremio+flight://test:test@localhost:32010/test")
        assert engine.dialect.name == "dremio+flight"
        assert engine.dialect.driver == "dremio+flight"
    
    def test_type_mapping_in_context(self, mock_engine):
        """Test type mapping works in engine context."""
        from sqlalchemy_dremio.flight import _type_map
        
        # Verify our enhanced type map is accessible
        assert len(_type_map) > 10  # Should have many type mappings
        assert 'varchar' in _type_map
        assert 'VARCHAR' in _type_map
        assert 'smallint' in _type_map
    
    @pytest.mark.skipif(
        not os.environ.get('DREMIO_CONNECTION_URL'), 
        reason="No live Dremio connection available"
    )
    def test_live_connection(self):
        """Test with live Dremio connection if available."""
        connection_url = os.environ.get('DREMIO_CONNECTION_URL')
        if not connection_url:
            pytest.skip("DREMIO_CONNECTION_URL not set")
        
        engine = create_engine(connection_url)
        try:
            with engine.connect() as conn:
                # Test basic connectivity
                result = conn.execute(text("SELECT 1 as test_col"))
                row = result.fetchone()
                assert row[0] == 1
                
                # Test schema introspection
                inspector = inspect(engine)
                schemas = inspector.get_schema_names()
                assert isinstance(schemas, list)
                
        except OperationalError as e:
            pytest.skip(f"Could not connect to Dremio: {e}")
        finally:
            engine.dispose()
    
    def test_inspector_methods_mock(self):
        """Test inspector methods with mocked connection."""
        from sqlalchemy_dremio.flight import DremioDialect_flight
        
        dialect = DremioDialect_flight()
        
        # Mock connection and cursor
        connection_mock = Mock()
        cursor_mock = Mock()
        
        # Test get_schema_names
        cursor_mock.__iter__ = Mock(return_value=iter([('schema1',), ('schema2',)]))
        connection_mock.execute.return_value = cursor_mock
        
        schemas = dialect.get_schema_names(connection_mock)
        assert schemas == ['schema1', 'schema2']
        
        # Verify the SQL was executed correctly
        connection_mock.execute.assert_called_with("SHOW SCHEMAS")
    
    def test_has_table_mock(self):
        """Test has_table method with mocked connection."""
        from sqlalchemy_dremio.flight import DremioDialect_flight
        
        dialect = DremioDialect_flight()
        connection_mock = Mock()
        cursor_mock = Mock()
        
        # Test table exists
        cursor_mock.__iter__ = Mock(return_value=iter([(1,)]))
        connection_mock.execute.return_value = cursor_mock
        
        result = dialect.has_table(connection_mock, "test_table", "test_schema")
        assert result is True
        
        # Test table doesn't exist
        cursor_mock.__iter__ = Mock(return_value=iter([(0,)]))
        connection_mock.execute.return_value = cursor_mock
        
        result = dialect.has_table(connection_mock, "nonexistent_table", "test_schema")
        assert result is False


class TestBackwardCompatibility:
    """Test backward compatibility with older versions."""
    
    def test_dbapi_import(self):
        """Test that dbapi can still be imported."""
        from sqlalchemy_dremio.flight import DremioDialect_flight
        
        dialect = DremioDialect_flight()
        dbapi = dialect.dbapi()
        
        # Should return the db module
        assert hasattr(dbapi, 'connect')
    
    def test_engine_properties(self):
        """Test that engine has expected properties."""
        engine = create_engine("dremio+flight://test:test@localhost:32010/test")
        
        # Test key properties
        assert engine.dialect.supports_sane_rowcount is False
        assert engine.dialect.supports_sane_multi_rowcount is False
        assert engine.dialect.paramstyle == 'pyformat'


def run_unit_tests_only():
    """Run only the unit tests that don't require a connection."""
    pytest.main([
        "test/test_unit.py", 
        "-v", 
        "--tb=short"
    ])


def run_integration_tests():
    """Run integration tests, skipping live connection tests if not available."""
    pytest.main([
        "test/test_integration.py",
        "-v", 
        "--tb=short"
    ])


def run_all_tests():
    """Run all tests."""
    pytest.main([
        "test/",
        "-v",
        "--tb=short"
    ])


if __name__ == "__main__":
    # Default to running unit tests only
    run_unit_tests_only()
