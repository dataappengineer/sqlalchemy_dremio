@echo off
REM Setup script for testing SQLAlchemy Dremio modifications
REM This script will help you set up the environment and run tests

echo ============================================================
echo SQLAlchemy Dremio - Setup and Test Script
echo ============================================================

REM Check if we're in the right directory
if not exist "setup.py" (
    echo Error: setup.py not found. Please run this from the project root directory.
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check Python version
echo Checking Python version...
python --version
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found. Please ensure Python is installed and in PATH.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Option 1: Quick Test (No Environment Setup)
echo ============================================================
echo This will test your modifications using the current Python environment.
echo.
choice /c YN /m "Run quick test now"
if %ERRORLEVEL%==1 (
    echo Running simple test...
    python test_simple.py
    echo.
    echo Test completed. Check results above.
    pause
)

echo.
echo ============================================================
echo Option 2: Install in Development Mode
echo ============================================================
echo This will install the package in development mode so changes are immediately available.
echo.
choice /c YN /m "Install package in development mode"
if %ERRORLEVEL%==1 (
    echo Installing package in development mode...
    pip install -e .
    if %ERRORLEVEL%==0 (
        echo.
        echo ✓ Package installed successfully!
        echo Now running tests...
        python test_simple.py
    ) else (
        echo ✗ Installation failed.
    )
    pause
)

echo.
echo ============================================================
echo Option 3: Create Virtual Environment
echo ============================================================
echo This will create a new virtual environment for testing.
echo.
choice /c YN /m "Create and setup virtual environment"
if %ERRORLEVEL%==1 (
    echo Creating virtual environment...
    python -m venv venv_test
    
    echo Activating virtual environment...
    call venv_test\Scripts\activate.bat
    
    echo Upgrading pip...
    python -m pip install --upgrade pip
    
    echo Installing package in development mode...
    pip install -e .
    
    if %ERRORLEVEL%==0 (
        echo.
        echo ✓ Environment setup complete!
        echo Running tests...
        python test_simple.py
        echo.
        echo To use this environment later, run:
        echo   venv_test\Scripts\activate.bat
    ) else (
        echo ✗ Setup failed.
    )
    pause
)

echo.
echo ============================================================
echo Manual Commands
echo ============================================================
echo If you prefer to run commands manually:
echo.
echo 1. Install in development mode:
echo    pip install -e .
echo.
echo 2. Run simple tests:
echo    python test_simple.py
echo.
echo 3. Run unit tests (if pytest available):
echo    python -m pytest test/test_unit.py -v
echo.
echo 4. Test with live connection (set DREMIO_CONNECTION_URL first):
echo    set DREMIO_CONNECTION_URL=dremio+flight://user:pass@host:port/db
echo    python test/test_integration.py
echo ============================================================

pause
