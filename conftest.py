"""conftest.py -- Configure pytest.
https://docs.pytest.org/en/reorganize-docs/example/simple.html#control-skipping-of-tests-according-to-command-line-option
"""

import pytest

def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
        help="run slow tests")