#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test runner for SQLAlchemy Dremio dialect.
Provides different test modes based on available resources.
"""
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that the dialect can be imported successfully."""
    print("Testing imports...")
    try:
        import sqlalchemy_dremio
        from sqlalchemy_dremio.flight import DremioDialect_flight, _type_map
        print("✓ Successfully imported sqlalchemy_dremio")
        print(f"✓ Type map has {len(_type_map)} entries")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_type_mappings():
    """Test the enhanced type mappings."""
    print("\nTesting type mappings...")
    from sqlalchemy_dremio.flight import _type_map
    from sqlalchemy import types
    
    # Test cases for the enhanced type map
    test_cases = [
        ('boolean', types.BOOLEAN),
        ('BOOLEAN', types.BOOLEAN),
        ('varchar', types.VARCHAR),
        ('VARCHAR', types.VARCHAR),
        ('smallint', types.SMALLINT),
        ('varbinary', types.LargeBinary),
        ('VARBINARY', types.LargeBinary),
        ('BINARY VARYING', types.VARBINARY),
        ('int', types.INTEGER),
        ('INTEGER', types.INTEGER),
    ]
    
    passed = 0
    for type_name, expected_type in test_cases:
        if type_name in _type_map and _type_map[type_name] == expected_type:
            print(f"✓ {type_name} -> {expected_type.__name__}")
            passed += 1
        else:
            print(f"✗ {type_name} mapping failed")
    
    print(f"Type mapping tests: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)


def test_dialect_properties():
    """Test dialect properties and methods."""
    print("\nTesting dialect properties...")
    from sqlalchemy_dremio.flight import DremioDialect_flight
    
    dialect = DremioDialect_flight()
    tests_passed = 0
    total_tests = 0
    
    # Test that supports_statement_cache is not False
    total_tests += 1
    supports_cache = getattr(dialect, 'supports_statement_cache', None)
    if supports_cache is not False:
        print("✓ supports_statement_cache properly configured")
        tests_passed += 1
    else:
        print("✗ supports_statement_cache still set to False")
    
    # Test that dbapi method exists
    total_tests += 1
    if hasattr(dialect, 'dbapi') and callable(dialect.dbapi):
        print("✓ dbapi method exists")
        tests_passed += 1
    else:
        print("✗ dbapi method missing")
    
    # Test that import_dbapi method is removed
    total_tests += 1
    if not hasattr(dialect, 'import_dbapi'):
        print("✓ import_dbapi method removed")
        tests_passed += 1
    else:
        print("✗ import_dbapi method still exists")
    
    # Test that do_execute method is removed
    total_tests += 1
    if not hasattr(dialect, 'do_execute'):
        print("✓ do_execute method removed")
        tests_passed += 1
    else:
        print("✗ do_execute method still exists")
    
    print(f"Dialect property tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests


def test_engine_creation():
    """Test that engines can be created without errors."""
    print("\nTesting engine creation...")
    try:
        from sqlalchemy import create_engine
        
        # Test basic engine creation
        engine = create_engine("dremio+flight://test:test@localhost:32010/test")
        print("✓ Engine created successfully")
        print(f"✓ Dialect name: {engine.dialect.name}")
        print(f"✓ Driver: {engine.dialect.driver}")
        print(f"✓ Paramstyle: {engine.dialect.paramstyle}")
        
        # Test that key properties are set correctly
        assert engine.dialect.supports_sane_rowcount is False
        assert engine.dialect.supports_sane_multi_rowcount is False
        print("✓ Dialect properties correctly configured")
        
        engine.dispose()
        return True
    except Exception as e:
        print(f"✗ Engine creation failed: {e}")
        return False


def run_unit_tests():
    """Run pytest unit tests if available."""
    print("\nRunning unit tests...")
    try:
        import pytest
        # Run unit tests
        exit_code = pytest.main([
            "test/test_unit.py",
            "-v",
            "--tb=short",
            "-q"
        ])
        return exit_code == 0
    except ImportError:
        print("pytest not available, skipping unit tests")
        return True
    except Exception as e:
        print(f"Unit tests failed: {e}")
        return False


def main():
    """Main test runner."""
    print("=" * 60)
    print("SQLAlchemy Dremio Dialect Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    # Run basic tests
    all_passed &= test_imports()
    all_passed &= test_type_mappings()
    all_passed &= test_dialect_properties()
    all_passed &= test_engine_creation()
    
    # Run unit tests if available
    all_passed &= run_unit_tests()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Your modifications are working correctly.")
        print("\nNext steps:")
        print("1. Install in development mode: pip install -e .")
        print("2. Test with a live Dremio connection if available")
        print("3. Set DREMIO_CONNECTION_URL environment variable for integration tests")
    else:
        print("❌ Some tests failed. Please review the output above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
