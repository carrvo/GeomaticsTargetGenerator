"""
Install all dependencies through pip.
"""

from pip import main as pip

def install():
    pip(['install', 'beautifulsoup4'])
    pip(['install', 'lxml'])
install.__doc__ = __doc__

#Built-in dependencies:
#   os, math, io.StringIO, cmd.Cmd, traceback, argparse.ArgumentParser
