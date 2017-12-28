"""
This module deals with interactive console editing.
"""

from cmd import Cmd

from .__init__ import *

class Console(Cmd):
    """
    Interactive Console for editing *.tdef.
    """

    def __init__(self, stdin=None, stdout=None):
        """
        Initializes.
        """
        super().__init__(stdin=stdin, stdout=stdout)
        self.primary_prompt = 'GTG>>> '
        self.secondary_prompt = 'GTG... '
        self.prompt = self.primary_prompt
        self.subcommand = None
        self.subcommand_state = None
        self.current_file = None
        self.current_target_definition = None
        self.available_names()

    def parseLine(self, line):
        cmd, arg, line = super().parseLine(line)
        cmd = cmd.lower()
        arg = arg.split(' ')
        if len(arg) == 1:
            arg = arg[0]
        elif len(arg) == 0:
            arg = None
        return (cmd, arg, line)
    parseLine.__doc__ = super().parseLine.__doc__

    def precmd(self, line):
        """
        Preprocessing of the line before command is called.
        """
        return line

    def default(self, line):
        """
        """
        if self.subcommand:
            if self.subcommand_state:
                cmd, arg, line = self.parseLine(line)
                self.subcommand(cmd, arg)
            else: #Subcommand is done
                self.prompt = self.primary_prompt
                self.subcommand = None
        else:
            super().default(line)

    def emptyline(self):
        """
        Determines behaviour when no command is entered.
        """
        pass

    def postcmd(self, stop, line):
        """
        Determines when the Interpreter loop stops.
        """
        if self.subcommand:
            self.prompt = self.secondary_prompt
        return stop or line == 'EOF'

    def do_exit(self, arg):
        """
        Stops the Interpreter loop.
        """
        return True

    def available_names(self):
        """
        Buffers available file names.
        """
        self.names = TargetFile.AvailableNames()

    def do_names(self, arg):
        """
        Lists all the available file names.
        """
        for name in self.names:
            print(name)

    def do_load(self, arg):
        """
        Loads file for current editing.
        If file does not exist then creates a new one.
        """
        self.current_file = TargetFile(arg)
        if arg in self.names:
            self.current_file.LoadTargetDefinition()
        else:
            print('New File:', arg)
            self.names.update(arg)

    def do_save(self, arg):
        """
        Saves the current Definition into the current file.
        Default is to save as Definition file.
        Options: Definition, Prievew (future), Print (future)
        """
        arg = arg.lower()
        if False:
            pass
        #elif arg == 'preview':
            #self.current_file.SavePreview(self.current_target_definition)
        #elif arg == 'print':
            #self.current_file.SaveForPrint(self.current_target_definition)
        else: #Definition
            self.current_file.SaveTargetDefinition(self.current_target_definition)

    def do_clear(self, arg):
        """
        Clears current Definition and current file.
        Optional: specify to clear just Definition or file.
        """
        arg = arg.lower()
        if arg == 'definition':
            self.current_target_definition = None
        elif arg == 'file':
            self.current_file = None
        else:
            self.current_file = None
            self.current_target_definition = None

    def do_modify(self, arg):
        """
        Modifies:
            - BarCode [+ ring level ordered outward]
            - Max Radius [+ new value]
            - Coloured Circle (future).
        """
        arg = arg.lower()
        if arg[:7] == 'barcode':
            self.subcommand = self.sub_barcode
            self.subcommand_state = self.current_target_definition.RemoveFrom(int(arg[7:]))
        elif arg[:10] == 'max radius':
            self.current_target_definition.ChangeMaxRadius(float(arg[10:]))
        #elif arg == 'coloured circle':
            #self.current_target_definition.GetColouredCircle(##)
        self.subcommand(self, None, '')

    def sub_barcode(self, cmd, arg):
        """
        Modifies a BarCode.
        """
        current = self.subcommand_state[0]
        if cmd == 'current':
            print('Current BarCode:', str(current))
        elif cmd == 'inner':
            current.ChangeRadii(float(arg), current.OuterRadius)
        elif cmd == 'outer':
            current.ChangeRadii(current.InnerRadius, float(arg))
        elif cmd == 'inner-outer':
            current.ChangeRadii(float(arg[0]), float(arg[1]))
        elif cmd == 'angles':
            current.ChangeAngles([float(angle) for angle in arg])
        elif cmd == 'code':
            current.ChangeCode(int(arg))
        elif cmd == 'previous':
            self.subcommand_state = [ self.current_target_definition.RemoveFrom(-1) ] + self.subcommand_state
        elif cmd == 'remove':
            self.subcommand_state = self.subcommand_state[1:]
        elif cmd == 'next':
            self.current_target_definition.Add(current)
            self.subcommand_state = self.subcommand_state[1:]
        elif cmd == 'done':
            for state in self.subcommand_state:
                self.current_target_definition.Add(current)
            self.subcommand_state = []
        else:
            print("""
                COMMANDS:
                help [/?] - print this message
                current - prints the current BarCode values
                inner <value> - changes the Inner Radius (%)
                outer <value> - changes the Outer Radius (%)
                inner-outer <value> <value> - changes both radii
                angles <value> [<value> [...]] - changes the code
                code <value> - (future) changes the code
                previous - edit previous, inward, BarCode
                remove - removes the current BarCode
                    and edit the next, outward, BarCode
                next - edit next, outward, BarCode
                done - finish editing BarCodes
            """)

    def do_addbarcode(self, arg):
        """
        Adds a BarCode to the current Definition.
        addbarcode <inner radius> <outer radius> <angle> [<angle> [...]]
        """
        self.current_target_definition.Add(BarCode(*tuple(arg)))

    def do_addcode(self, arg):
        """
        Adds a BarCode to the current Definition.
        addcode <inner radius> <outer radius> <code>
        """
        self.current_target_definition.Add(BarCode(arg[0], arg[1], arg[2], coded=True))

    def do_circles(self, arg):
        """
        (future)
        """
        self.subcommand = self.sub_circles
        self.subcommand_state = 'editing'
        self.subcommand(self, None, '')

    def sub_circles(self, arg):
        """
        (future)
            - add
            - remove
            - modify
        """
        self.subcommand = None
        self.subcommand_state = None
