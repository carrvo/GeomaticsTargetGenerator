"""
Default for running tests.
"""

try:
    from Tests import run_tests
except ImportError:
    try:
        from . import context
    except ImportError:
        import context
    from Tests import run_tests

run_tests()
