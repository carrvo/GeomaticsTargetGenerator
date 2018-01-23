"""
Install all dependencies through pip.
"""

from pip import main as pip

DEPENDENCIES = [
    'beautifulsoup4',
    'lxml'
]

def install():
    for dependency in DEPENDENCIES:
        pip(['install', dependency])
install.__doc__ = __doc__

#Built-in dependencies:
#
#not yet:
#   os, math, io.StringIO, cmd.Cmd, traceback, argparse.ArgumentParser
