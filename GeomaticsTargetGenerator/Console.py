"""
This module deals with interactive console editing.
"""

from cmd import Cmd
import traceback

from .__api__ import API

class Console(Cmd):
    """
    Interactive Console for editing *.tdef.
    """

    def __init__(self, stdin=None, stdout=None):
        """
        Initializes.
        """
        super(Cmd, self).__thisclass__.__init__(self, stdin=stdin, stdout=stdout)
        self.primary_prompt = 'GTG>>> '
        self.secondary_prompt = 'GTG... '
        self.prompt = self.primary_prompt
        self.subcommand = None
        self.subcommand_state = None
        self.api = API()
        self.names = self.api.AvailableNames() #Buffers available file names.

    def parseline(self, line):
        cmd, arg, line = super().parseline(line)
        cmd = cmd.lower()
        arg = arg.split(' ')
        if len(arg) == 1:
            arg = arg[0]
        elif len(arg) == 0:
            arg = None
        return (cmd, arg, line)
    parseline.__doc__ = Cmd.parseline.__doc__

    def precmd(self, line):
        """
        Preprocessing of the line before command is called.
        """
        return line

    def onecmd(self, line):
        try:
            if self.subcommand:
                cmd, arg, line = self.parseline(line)
                return self.subcommand(cmd, arg)
            else:
                return super().onecmd(line)
        except Exception:
            traceback.print_exc()
            print()
            super().default(line)
    onecmd.__doc__ = Cmd.onecmd.__doc__

    def default(self, line):
        super().default(line)
    default.__doc__ = Cmd.__doc__

    def emptyline(self):
        """
        Determines behaviour when no command is entered.
        """
        pass

    def postcmd(self, stop, line):
        """
        Determines when the Interpreter loop stops.
        """
        if not self.subcommand_state: #Subcommand is done
            self.prompt = self.primary_prompt
            self.subcommand = None
        if self.subcommand:
            self.prompt = self.secondary_prompt
        return stop or line == 'EOF'

    def do_exit(self, arg):
        """
        Stops the Interpreter loop.
        """
        return True

    def do_names(self, arg):
        """
        Lists all the available file names.
        """
        for name in self.names:
            print(name)

    def do_load(self, arg):
        self.api.load(arg)
        if arg not in self.names:
            print('New File:', arg)
            self.names.update({arg})
    do_load.__doc__ = API.load.__doc__

    def do_save(self, arg):
        self.api.save(arg)
    do_save.__doc__ = API.save.__doc__

    def do_clear(self, arg):
        self.api.clear(arg)
    do_clear.__doc__ = API.clear.__doc__

    def do_remove(self, arg):
        self.api.remove()
    do_remove.__doc__ = API.remove.__doc__

    def do_modify(self, arg):
        """
        Modifies:
            - BarCode [+ ring level ordered outward]
            - MaxRadius [+ new value]
            - ColouredCircle (future).
        """
        mod, level = (arg[0].lower(), arg[1])
        if mod == 'barcode':
            self.subcommand = self.sub_barcode
            self.subcommand_state = self.api.modify(mod, int(level))
        elif mod == 'maxradius':
            self.api.modify(mod, float(level))
        elif mod == 'colouredcircle':
            self.api.modify(mod, int(level)) #GetColouredCircle(level)
        if self.subcommand:
            self.subcommand(None, '')

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
            current.ChangeAngles(
                [float(angle) for angle in arg if angle.find('=') == -1],
                angular_units= arg[-1].split('=')[1] if arg[-1].find('=') != -1 else 'radians'
            )
        elif cmd == 'code':
            current.ChangeCode(int(arg))
        elif cmd == 'previous':
            self.subcommand_state = self.api.modify('barcode', -1) + self.subcommand_state
        elif cmd == 'remove':
            self.subcommand_state = self.subcommand_state[1:]
        elif cmd == 'next':
            self.api.addbarcodeobject(current)
            self.subcommand_state = self.subcommand_state[1:]
        elif cmd == 'done':
            for state in self.subcommand_state:
                self.api.addbarcodeobject(state)
            self.subcommand_state = []
        else:
            print("""
                COMMANDS:
                help [/?] - print this message
                current - prints the current BarCode values
                inner <value> - changes the Inner Radius (%)
                outer <value> - changes the Outer Radius (%)
                inner-outer <value> <value> - changes both radii
                angles <value> [<value> [...]] [angular_units=radians]
                    - changes the code
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
        addbarcode <inner radius> <outer radius> <angle> [<angle> [...]] [kwarg=value [...]]
        """
        #args = (a if a.find('=') == -1 for a in arg)
        #kwargs = {a.split('=')[0]:a.split('=')[1] if a.find('=') != -1 for a in arg}
        args = (float(arg[0]), float(arg[1])) + tuple(float(a) for a in arg[2:] if a.find('=') == -1)
        kwargs = {a.split('=')[0]:a.split('=')[1]for a in arg[3:] if a.find('=') != -1}
        self.api.addbarcode(*args, **kwargs)

    def do_addcode(self, arg):
        """
        Adds a BarCode to the current Definition.
        addcode <inner radius> <outer radius> <code>
        """
        self.api.addcode(float(arg[0]), float(arg[1]), int(arg[2]))

    def do_circles(self, arg):
        """
        (future)
        ! Move to under do_modify !
        """
        self.subcommand = self.sub_circles
        self.subcommand_state = 'editing'
        self.subcommand(None, '')

    def sub_circles(self, cmd, arg):
        """
        (future)
            - add
            - remove
            - modify
        """
        self.subcommand = None
        self.subcommand_state = None
