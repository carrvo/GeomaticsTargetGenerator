"""
This module specifies commandline usage.
"""

from argparse import ArgumentParser
from io import StringIO

from .__init__ import *
from .Console import Console

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
arguments.add_argument('-F' '--file', action='store',
                        type=lambda name: open(name, 'rt', encoding='utf-8')
                        help="Use commands from a file")

if __name__ == '__main__':
    args = arguments.parse_args()
    if args.names:
        for name in Storage.AvailableNames():
            print(name)
    console = None
    if args.interactive:
        console = Console()
    elif args.commands:
        console = Console(stdin=StringIO('\n'.join(args.commands)))
    elif args.file:
        console = Console(stdin=args.file)
    if console:
        console.cmdLoop()
    if args.preview:
        file = Storage(args.preview)
        target_definition = file.LoadTargetDefinition()
        file.SavePreview(targetdefinition)
    if args.print:
        file = Storage(args.print)
        target_definition = file.LoadTargetDefinition()
        file.SaveForPrint(target_definition)
