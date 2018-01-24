"""
"""

from .AttributeSupport import AttributeSupport
from .ErrorBuilder import ParameterError

class Pair(AttributeSupport):
    """
    Represents an (x,y) pair for general use.
    """

    def __init__(self, x, y):
        """
        Initializes.
        """
        #want immutable to prevent external influence
        self.__x_y__ = (x, y)

    def x():
        doc = "The x property."
        def fget(self):
            return self.__x_y__[0]
        return locals()
    x = property(**x())

    def y():
        doc = "The y property."
        def fget(self):
            return self.__x_y__[1]
        return locals()
    y = property(**y())

    def __xml_repr__(self):
        return ','.join((str(self.x), str(self.y)))
    __xml_repr__.__doc__ = AttributeSupport.__xml_repr__.__doc__

    @classmethod
    def __xml_eval__(cls, string):
        string = string.split(',')
        return cls(int(string[0]), int(string[1]))
    __xml_eval__.__doc__ = AttributeSupport.__xml_eval__.__doc__
setattr(Pair, '__error__', ParameterError.CreateError(Pair))

class Point(Pair):
    """
    Represents a Pair of coordinates on the image.
    """
    pass
setattr(Point, '__error__', ParameterError.CreateError(Point))
