"""
This module specifies shell usage.
"""

from argparse import ArgumentParser
from io import StringIO

try:
    from . import __context__
except ImportError:
    import __context__
try:
    from GeomaticsTargetGenerator import *
    from GeomaticsTargetGenerator.Console import Console
except ImportError:
    DOC = "MISSING DEPENDENCIES -- PLEASE RUN 'python GeomaticsTargetGenerator -D' FIRST"
from __pip__ import install

INTERACTIVE_DOC = """
PRECEDENCE:
names
interactive/commands/file
preview
print
"""

arguments = ArgumentParser(description=DOC+INTERACTIVE_DOC)
arguments.add_argument('-a', '--names', action='store_true',
                        help="Print the names of available files")
arguments.add_argument('-p', '--preview', action='store', type=str,
                        help="(future) Creates a preview file")
arguments.add_argument('-P', '--print', action='store', type=str,
                        help="(future) Creates a printable file")
arguments.add_argument('-i', '--interactive', action='store_true',
                        help="Run Interactive Console")
arguments.add_argument('-c', '--commands', action='store', nargs='+',
                        help="Runs commands instead")
arguments.add_argument('-F', '--file', action='store',
                        type=lambda name: open(name, 'rt', encoding='utf-8'),
                        help="Use commands from a file")
arguments.add_argument('-D', '--dependencies', action='store_true',
                        help="Install dependencies through pip")

if __name__ == '__main__':
    args = arguments.parse_args()
    if args.dependencies:
        install()
        from GeomaticsTargetGenerator import *
        from GeomaticsTargetGenerator.Console import Console
    if args.names:
        for name in TargetFile.AvailableNames():
            print(name)
    console = None
    if args.interactive:
        console = Console()
    elif args.commands:
        console = Console(stdin=StringIO('\n'.join(args.commands)))
    elif args.file:
        console = Console(stdin=args.file)
    if console:
        console.cmdloop()
    if args.preview:
        file = Storage(args.preview)
        target_definition = file.LoadTargetDefinition()
        file.SavePreview(targetdefinition)
    if args.print:
        file = Storage(args.print)
        target_definition = file.LoadTargetDefinition()
        file.SaveForPrint(target_definition)
