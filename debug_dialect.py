#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug test to identify the exact issues with the dialect.
"""

def debug_dialect_issues():
    """Debug the dialect issues found in the test."""
    print("Debugging dialect issues...")
    
    try:
        from sqlalchemy_dremio.flight import DremioDialect_flight
        from sqlalchemy import create_engine
        
        # Test 1: Check the class directly
        print("\n1. Testing dialect class directly:")
        dialect = DremioDialect_flight()
        
        print(f"   - Has dbapi attribute: {hasattr(dialect, 'dbapi')}")
        print(f"   - dbapi is callable: {callable(getattr(dialect, 'dbapi', None))}")
        print(f"   - dbapi method type: {type(getattr(dialect, 'dbapi', None))}")
        
        # Try to call dbapi
        try:
            dbapi_module = dialect.dbapi()
            print(f"   - dbapi() call successful: {dbapi_module}")
            print(f"   - dbapi module has connect: {hasattr(dbapi_module, 'connect')}")
        except Exception as e:
            print(f"   - dbapi() call failed: {e}")
        
        # Check for do_execute
        print(f"   - Has do_execute: {hasattr(dialect, 'do_execute')}")
        if hasattr(dialect, 'do_execute'):
            print(f"   - do_execute type: {type(getattr(dialect, 'do_execute'))}")
        
        # Check paramstyle
        print(f"   - paramstyle: {dialect.paramstyle}")
        
        # Test 2: Check via engine
        print("\n2. Testing via engine:")
        engine = create_engine("dremio+flight://test:test@localhost:32010/test")
        
        print(f"   - Engine dialect has dbapi: {hasattr(engine.dialect, 'dbapi')}")
        print(f"   - Engine dialect dbapi callable: {callable(getattr(engine.dialect, 'dbapi', None))}")
        print(f"   - Engine paramstyle: {engine.dialect.paramstyle}")
        print(f"   - Engine dialect has do_execute: {hasattr(engine.dialect, 'do_execute')}")
        
        # Try dbapi from engine
        try:
            dbapi_from_engine = engine.dialect.dbapi()
            print(f"   - Engine dbapi() call successful: {dbapi_from_engine}")
        except Exception as e:
            print(f"   - Engine dbapi() call failed: {e}")
        
        # Test 3: Check class methods vs instance methods
        print("\n3. Testing class vs instance methods:")
        print(f"   - Class has dbapi: {hasattr(DremioDialect_flight, 'dbapi')}")
        print(f"   - Class dbapi is classmethod: {'classmethod' in str(type(getattr(DremioDialect_flight, 'dbapi', None)))}")
        
        # Test 4: Check parent class
        print("\n4. Checking parent class:")
        from sqlalchemy.engine import default
        parent_dialect = default.DefaultDialect()
        print(f"   - Parent has dbapi: {hasattr(parent_dialect, 'dbapi')}")
        print(f"   - Parent has do_execute: {hasattr(parent_dialect, 'do_execute')}")
        print(f"   - Parent paramstyle: {getattr(parent_dialect, 'paramstyle', 'Not set')}")
        
        engine.dispose()
        
    except Exception as e:
        print(f"Debug failed: {e}")
        import traceback
        traceback.print_exc()


def check_method_resolution():
    """Check method resolution order for the dialect."""
    print("\n" + "="*50)
    print("Method Resolution Order Debug")
    print("="*50)
    
    try:
        from sqlalchemy_dremio.flight import DremioDialect_flight
        
        print("MRO for DremioDialect_flight:")
        for i, cls in enumerate(DremioDialect_flight.__mro__):
            print(f"  {i}: {cls}")
            if hasattr(cls, 'dbapi'):
                print(f"     -> has dbapi method")
            if hasattr(cls, 'do_execute'):
                print(f"     -> has do_execute method")
        
        # Check what methods are actually available
        print(f"\nAll methods containing 'dbapi':")
        for attr_name in dir(DremioDialect_flight):
            if 'dbapi' in attr_name.lower():
                attr = getattr(DremioDialect_flight, attr_name)
                print(f"  {attr_name}: {type(attr)}")
        
        print(f"\nAll methods containing 'execute':")
        for attr_name in dir(DremioDialect_flight):
            if 'execute' in attr_name.lower():
                attr = getattr(DremioDialect_flight, attr_name)
                print(f"  {attr_name}: {type(attr)}")
                
    except Exception as e:
        print(f"MRO check failed: {e}")


if __name__ == "__main__":
    debug_dialect_issues()
    check_method_resolution()
