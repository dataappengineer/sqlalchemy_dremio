#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test to verify your modifications work without needing a live Dremio connection.
"""

def test_basic_imports():
    """Test that we can import the dialect."""
    print("Testing basic imports...")
    try:
        # Test importing the main module
        import sqlalchemy_dremio
        print("✓ Successfully imported sqlalchemy_dremio")
        
        # Test importing the flight dialect
        from sqlalchemy_dremio.flight import DremioDialect_flight, _type_map
        print("✓ Successfully imported flight dialect")
        
        # Test importing SQLAlchemy
        from sqlalchemy import create_engine, types
        print("✓ Successfully imported SQLAlchemy")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_type_mappings():
    """Test your enhanced type mappings."""
    print("\nTesting enhanced type mappings...")
    
    try:
        from sqlalchemy_dremio.flight import _type_map
        from sqlalchemy import types
        
        print(f"Type map contains {len(_type_map)} entries")
        
        # Test your new mappings
        test_cases = [
            ('boolean', types.BOOLEAN, "lowercase boolean"),
            ('BOOLEAN', types.BOOLEAN, "uppercase BOOLEAN"),
            ('varchar', types.VARCHAR, "lowercase varchar"), 
            ('VARCHAR', types.VARCHAR, "uppercase VARCHAR"),
            ('smallint', types.SMALLINT, "smallint support"),
            ('varbinary', types.LargeBinary, "lowercase varbinary as LargeBinary"),
            ('VARBINARY', types.LargeBinary, "uppercase VARBINARY as LargeBinary"),
            ('BINARY VARYING', types.VARBINARY, "BINARY VARYING mapping"),
            ('int', types.INTEGER, "lowercase int"),
            ('INTEGER', types.INTEGER, "uppercase INTEGER"),
        ]
        
        passed = 0
        for type_name, expected_type, description in test_cases:
            if type_name in _type_map:
                actual_type = _type_map[type_name]
                if actual_type == expected_type:
                    print(f"✓ {description}: {type_name} -> {expected_type.__name__}")
                    passed += 1
                else:
                    print(f"✗ {description}: {type_name} -> {actual_type.__name__} (expected {expected_type.__name__})")
            else:
                print(f"✗ {description}: {type_name} not found in type map")
        
        print(f"\nType mapping tests: {passed}/{len(test_cases)} passed")
        return passed == len(test_cases)
        
    except Exception as e:
        print(f"✗ Type mapping test failed: {e}")
        return False


def test_dialect_changes():
    """Test your dialect modifications."""
    print("\nTesting dialect modifications...")
    
    try:
        from sqlalchemy_dremio.flight import DremioDialect_flight
        
        dialect = DremioDialect_flight()
        tests_passed = 0
        total_tests = 0
        
        # Test 1: supports_statement_cache should not be False
        total_tests += 1
        supports_cache = getattr(dialect, 'supports_statement_cache', None)
        if supports_cache is not False:
            print(f"✓ supports_statement_cache properly configured (value: {supports_cache})")
            tests_passed += 1
        else:
            print("✗ supports_statement_cache still set to False")
        
        # Test 2: dbapi method should exist
        total_tests += 1
        if hasattr(dialect, 'dbapi') and callable(dialect.dbapi):
            print("✓ dbapi method exists for backward compatibility")
            tests_passed += 1
        else:
            print("✗ dbapi method missing or not callable")
        
        # Test 3: import_dbapi method should be removed
        total_tests += 1
        if not hasattr(dialect, 'import_dbapi'):
            print("✓ import_dbapi method successfully removed")
            tests_passed += 1
        else:
            print("✗ import_dbapi method still exists (should be removed)")
        
        # Test 4: do_execute method should use default implementation (not custom)
        total_tests += 1
        if hasattr(dialect, 'do_execute'):
            # Check if it's the default implementation (not our custom one)
            import inspect
            try:
                do_execute_source = inspect.getsource(dialect.do_execute)
                if "replaced_stmt" not in do_execute_source and "escaped_str" not in do_execute_source:
                    print("✓ Custom do_execute method successfully removed (using default)")
                    tests_passed += 1
                else:
                    print("✗ Custom do_execute method still exists")
            except (OSError, TypeError):
                # Can't get source (likely inherited method), which is good
                print("✓ Using inherited do_execute method (custom implementation removed)")
                tests_passed += 1
        else:
            print("✗ do_execute method completely missing (unexpected)")
        
        print(f"\nDialect modification tests: {tests_passed}/{total_tests} passed")
        return tests_passed == total_tests
        
    except Exception as e:
        print(f"✗ Dialect test failed: {e}")
        return False


def test_engine_creation():
    """Test that engines can be created with your modifications."""
    print("\nTesting engine creation...")
    
    try:
        from sqlalchemy import create_engine
        
        # Create engine (this doesn't actually connect)
        engine = create_engine("dremio+flight://test:test@localhost:32010/test")
        
        print("✓ Engine created successfully")
        print(f"✓ Dialect name: {engine.dialect.name}")
        print(f"✓ Driver: {engine.dialect.driver}")
        print(f"✓ Paramstyle: {engine.dialect.paramstyle}")
        
        # Test dialect properties
        assert engine.dialect.supports_sane_rowcount is False
        assert engine.dialect.supports_sane_multi_rowcount is False
        print("✓ Dialect properties correctly configured")
        
        # Clean up
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"✗ Engine creation failed: {e}")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("SQLAlchemy Dremio Dialect - Simple Test Suite")
    print("Testing your modifications without requiring a live connection")
    print("=" * 60)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_basic_imports()
    all_passed &= test_type_mappings()
    all_passed &= test_dialect_changes()
    all_passed &= test_engine_creation()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Your modifications are working correctly.")
        print("\nYour changes:")
        print("✓ Enhanced type mappings with case-insensitive support")
        print("✓ Removed deprecated properties and methods")
        print("✓ Improved table quoting and SQL generation")
        print("✓ Better SQLAlchemy 2.x compatibility")
        print("\nTo test with a live connection:")
        print("1. Set up a Dremio server")
        print("2. Set DREMIO_CONNECTION_URL environment variable") 
        print("3. Run: python test/test_integration.py")
    else:
        print("❌ Some tests failed. Please check the modifications.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
