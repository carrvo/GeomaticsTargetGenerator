"""
"""

from .Poly import Polyline
from .Pair import Point
from .ErrorBuilder import ParameterError
from .__magic__ import xmlrepr

class CommandError(TypeError):
    """
    """
    def __str__(self):
        return 'Command is missing.'

class PathSegment(Point):
    """
    """

    __error__ = ParameterError.CreateError(__class__)
    __command__ = None

    def __init__(self, x, y, isabsolute=False):
        """
        Initializes.
        """
        super().__init__(x, y)
        self.isabsolute = isabsolute

    @def command():
        doc = "The command property."
        def fget(self):
            if not PathSegment.__command__:
                raise CommandError()
            if self.isabsolute:
                return PathSegment.__command__
            else:
                return PathSegment.__command__.lower()
        return locals()
    command = property(**command())

    def __xml_repr__(self):
        return self.command + xmlrepr(super())
    __xml_repr__.__doc__ = Point.__xml_repr__.__doc__

    @classmethod
    def __xml_eval__(cls, string):
        command = string[0]
        if command == ClosePath.command:
            return ClosePath()
        string = string[1:].split(',')
        return PathCommand.__all__[command](int(string[0]), int(string[1]), command.isupper())
    __xml_eval__.__doc__ = Point.__xml_eval__.__doc__

class PathSegmentCLOSE(PathSegment):
    """
    Special PathSegment that closes the path.
    Does not require a position.
    """
    def __init__(self):
        self.isabsolute = True
    def __xml_repr__(self):
        return self.command

class PathCommand(object):
    """
    """

    __all__ = {}

    def __init__(self, command):
        """
        Initializes.
        """
        self.command = command.upper()
        PathCommand.__all__.update({self.command:self})

    def __call__(self):
        class Temp(PathSegment):
            __command__ = self.command
        Temp.__class__.__name__ = self.__class__.__name__ + self.command
        return Temp

    def __getattr__(self, name):
        """
        Treat the commands as methods.
        """
        return self.__class__.__all__[name]

#COMMANDS
MoveTo = PathCommand('M')
LineTo = PathCommand('L')
HorizontalLineTo = PathCommand('H')
VerticalLineTo = PathCommand('V')
CurveTo = PathCommand('C')
SmoothCurveTo = PathCommand('S')
QuadraticBezierCurveTo = PathCommand('Q')
SmoothQuadraticBezierCurveTo = PathCommand('T')
EllipticalArcTo = PathCommand('A')
ClosePath = PathCommand('Z')
ClosePath.__class__ = PathSegmentCLOSE

class Path(Polyline):
    """
    """

    __tag_name__ = 'path'
    __tag_attrs__ = {
        'd':[]
    }
    __svg_attrs__ = {}
    __list_type__ = PathSegment

    def __init__(self, segments=[], style=None):
        """
        Initializes.
        """
        super().__init__(segments, style=style)

    def addSegment(self, command):
        self.points.append(check(self.__class__.__list_type__, command))
