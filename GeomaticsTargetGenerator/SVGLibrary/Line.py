"""
"""

from .BaseSVG import BaseSVG
from .Pair import Point

class Line(BaseSVG):
    """
    """

    __tag_name__ = 'line'
    __tag_attrs__ = {
        'x1':0,
        'y1':0,
        'x2':0,
        'y2':0
    }
    __svg_attrs__ = {
        'position1':Point,
        'position2':Point
    }

    def __init__(self, position1, position2, style=None):
        """
        Initializes.
        """
        super().__init__(
            position1=position1,
            position2=position2,
            style=style
        )

    #short-cuts

    def x1():
        doc = "The x1 property."
        def fget(self):
            return self.position1.x
        def fset(self, value):
            self.position1 = Point(value, self.y1)
        return locals()
    x1 = property(**x1())

    def y1():
        doc = "The y1 property."
        def fget(self):
            return self.position1.y
        def fset(self, value):
            self.position1 = Point(self.x1, value)
        return locals()
    y1 = property(**y1())

    def x2():
        doc = "The x2 property."
        def fget(self):
            return self.position2.x
        def fset(self, value):
            self.position2 = Point(value, self.y2)
        return locals()
    x2 = property(**x2())

    def y2():
        doc = "The y2 property."
        def fget(self):
            return self.position2.y
        def fset(self, value):
            self.position2 = Point(self.x2, value)
        return locals()
    y2 = property(**y2())
