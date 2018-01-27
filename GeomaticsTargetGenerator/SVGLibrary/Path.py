"""
"""

from .Poly import Polyline
from .Pair import Point
from .ErrorBuilder import ParameterError
from .__magic__ import xmlrepr, check

class CommandError(TypeError):
    """
    """
    def __str__(self):
        return 'Command is missing.'

class PathSegment(Point):
    """
    """

    __command__ = None

    def __init__(self, x, y, *args, isabsolute=False):
        """
        Initializes.
        """
        super(Point, self).__thisclass__.__init__(self, x, y)
        self.isabsolute = isabsolute
        self.additional_arguments = args

    def command():
        doc = "The command property."
        def fget(self):
            if not self.__class__.__command__:
                raise CommandError()
            if self.isabsolute:
                return self.__class__.__command__
            else:
                return self.__class__.__command__.lower()
        return locals()
    command = property(**command())

    def __xml_repr__(self):
        return self.command + xmlrepr(super(Point, self).__thisclass__, self) + ' ' + ' '.join((str(arg) for arg in self.additional_arguments))
    __xml_repr__.__doc__ = Point.__xml_repr__.__doc__

    @classmethod
    def __xml_eval__(cls, string):
        command = string[0]
        if command == ClosePath.command:
            return ClosePath()
        string = string[1:].split(',')
        return PathCommand[command](int(string[0]), int(string[1]), command.isupper())
    __xml_eval__.__doc__ = Point.__xml_eval__.__doc__
setattr(PathSegment, '__error__', ParameterError.CreateError(PathSegment))

class PathSegmentCLOSE(PathSegment):
    """
    Special PathSegment that closes the path.
    Does not require a position.
    """
    def __init__(self):
        self.isabsolute = True
    def __xml_repr__(self):
        return self.command

class DynamicCommands(type):
    """
    Apparently you cannot do:
        - @classmethod def __getattr__(cls, key)
        - @classmethod def __getitem__(cls, key)
    https://stackoverflow.com/questions/3155436/getattr-for-static-class-variables-in-python
    """
    def __init__(cls, name, bases, namespace):
        super(DynamicCommands, cls).__init__(name, bases, namespace)
        cls.__backward__ = {}
        cls.__commands__ = {}
    def __getitem__(cls, key):
        return cls.__backward__[key.upper()]
    def __getattr__(cls, key):
        return cls.__commands__[key]

class PathCommand(object, metaclass=DynamicCommands):
    """
    """

    def __init__(self, command):
        """
        Initializes.
        """
        self.command = command.upper()
        self.__class__.__backward__.update({self.command:self})
        class Temp(PathSegment):
            __command__ = self.command
        Temp.__name__ = self.__class__.__name__ + self.command
        self.__klass__ = Temp

    def __call__(self, *args, **kwargs):
        # Quick-fix for original intention not what was actually coded
        # Initializer should just return self.__klass__ instead --> but find better solution
        return self.__klass__(*args, **kwargs)

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
#COMMANDS MAPPED
PathCommand.__commands__ = {
    'MoveTo':MoveTo,
    'LineTo':LineTo,
    'HorizontalLineTo':HorizontalLineTo,
    'VerticalLineTo':VerticalLineTo,
    'CurveTo':CurveTo,
    'SmoothCurveTo':SmoothCurveTo,
    'QuadraticBezierCurveTo':QuadraticBezierCurveTo,
    'SmoothQuadraticBezierCurveTo':SmoothQuadraticBezierCurveTo,
    'EllipticalArcTo':EllipticalArcTo,
    'ClosePath':ClosePath
}

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
        super(Polyline, self).__thisclass__.__init__(self, segments, style=style)

    def segments():
        doc = "The segments property."
        def fget(self):
            return self.points
        def fset(self, value):
            self.points = value
        return locals()
    segments = property(**segments())

    def addSegment(self, command):
        self.segments.append(check(self.__class__.__list_type__, command))
