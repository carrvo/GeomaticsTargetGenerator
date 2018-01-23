"""
"""

from .BaseSVG import BaseSVG

class Rectangle(BaseSVG):
    """
    """

    __tag_name__ = 'rect'
    __tag_attrs__ = {
        'x':0,
        'y':0,
        'rx':0,
        'ry':0,
        'width':0,
        'height':0
    }
    __svg_attrs__ = {
        'position':Point,
        'size':Pair,
        'rounded':Pair
    }

    def __init__(self, position, size, rounded=Pair(0, 0), style=None):
        """
        Initializes.
        """
        super().__init__(
            position=position,
            size=size,
            rounded=rounded,
            style=style
        )

    #short-cuts

    @def x():
        doc = "The x property."
        def fget(self):
            return self.position.x
        def fset(self, value):
            self.position = Point(value, self.y)
        return locals()
    x = property(**x())

    @def y():
        doc = "The y property."
        def fget(self):
            return self.position.y
        def fset(self, value):
            self.position = Point(self.x, value)
        return locals()
    y = property(**y())

    @def rx():
        doc = "The rx property."
        def fget(self):
            return self.rounded.x
        def fset(self, value):
            self.rounded = Pair(value, self.ry)
        return locals()
    rx = property(**rx())

    @def ry():
        doc = "The ry property."
        def fget(self):
            return self.rounded.y
        def fset(self, value):
            self.rounded = Pair(self.rx, value)
        return locals()
    ry = property(**ry())

    @def width():
        doc = "The width property."
        def fget(self):
            return self.size.x
        def fset(self, value):
            self.size = Pair(value, self.height)
        return locals()
    width = property(**width())

    @def height():
        doc = "The height property."
        def fget(self):
            return self.size.y
        def fset(self, value):
            self.size = Pair(self.width, value)
        return locals()
    height = property(**height())
