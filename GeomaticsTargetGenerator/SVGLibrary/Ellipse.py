"""
"""

from .BaseSVG import BaseSVG
from .Pair import Pair, Point

class Ellipse(BaseSVG):
    """
    """

    __tag_name__ = 'ellipse'
    __tag_attrs__ = {
        'cx':0,
        'cy':0,
        'rx':0,
        'ry':0
    }
    __svg_attrs__ = {
        'center':Point,
        'radius':Pair
    }

    def __init__(self, centerX, centerY, radiusX, radiusY, style=None):
        """
        Initializes.
        """
        super().__init__(center=center, radius=radius, style=style)

    #short-cuts

    def cx():
        doc = "The cx property."
        def fget(self):
            return self.center.x
        return locals()
    cx = property(**cx())

    def cy():
        doc = "The cy property."
        def fget(self):
            return self.center.y
        return locals()
    cy = property(**cy())

    def rx():
        doc = "The rx property."
        def fget(self):
            return self.radius.x
        return locals()
    rx = property(**rx())

    def ry():
        doc = "The ry property."
        def fget(self):
            return self.radius.y
        return locals()
    ry = property(**ry())
