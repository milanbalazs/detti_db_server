#Tests
The database and the server are tested separately.

**The UnitTest file of the database:**
 - `test/test_db_ut.py`

**The UnitTest file of the server:**
 - `test/test_server_ut_local.py`

**The used UT config file:**
 - `test/detti_conf_ut.ini`

##Run tests

You can run the all test with the `test/unit_test_runner.sh` runner script.

**The `test/unit_test_runner.sh` script does:**
 - Generate the Python3 virtual environment
 - Update the Python3 virtual environment based on the requirement.txt file
 - Activate the Python3 virtual environment
 - Starting the Detti Server
 - Start the all Unit tests with the `*_ut*.py` pattern in the `test` folder.
 - Generate coverage reports
 - After the running:
    - Deactivate the Python virtual environment
    - Kill all precesses which has started from runner script

**You can run the UnitTests by hand if you simply call with Python interpreter:**
 - Eg.: `python3 test/test_db_ut.py`
 - **In this case you have to prepare the environment for tests!**

**The related UnitTests can run in a GitHub action:**
 - The YML file of the GitHub action:
    - `.github/workflows/python_unittest.yml`

##Results
 - After successful running you can open the generated UT coverage HTML report:
    - `firefox htmlcov/index.html`
 - XML coverage report is available:
    - `coverage_reports/coverage_python.xml`
