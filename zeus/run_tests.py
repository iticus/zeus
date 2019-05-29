"""
Created on May 29, 2019

@author: ionut
"""

import logging
import sys
import unittest
logging.basicConfig(level=logging.WARNING)


def main():
    """Load all tests from "tests" folder and run them"""
    pattern = 'test*.py'
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
    loader = unittest.TestLoader()
    tests = loader.discover("tests", pattern=pattern)
    test_runner = unittest.runner.TextTestRunner()  # verbosity=2
    test_runner.run(tests)


if __name__ == "__main__":
    main()
