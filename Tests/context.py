"""
Used to allow tests to be run inside folder instead of imported from parent.

Usage:
import context
import <package> #would fail otherwise
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
