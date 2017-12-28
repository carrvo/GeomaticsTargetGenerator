"""
NORMAL:
from sqliteclass.tests import run_tests
run_tests()

TEST SUITE:
from sqliteclass.tests import test_suite
"""

import unittest
from Tests.MainThoroughfair import TargetDefinitionLifeCycle

#http://stackoverflow.com/questions/12011091/trying-to-implement-python-testsuite
test_suite = unittest.TestSuite()
for test in [
                TargetDefinitionLifeCycle,
            ]:
    test_suite.addTest(unittest.makeSuite(test))
runner = unittest.TextTestRunner()
run_tests = lambda: runner.run(test_suite)

__all__ = ["run_tests", "test_suite"]
