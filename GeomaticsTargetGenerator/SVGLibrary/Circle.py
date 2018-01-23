"""
"""

from .BaseSVG import BaseSVG

class Circle(BaseSVG):
    """
    """

    __tag_name__ = 'circle'
    __tag_attrs__ = {
        'cx':0,
        'cy':0,
        'r':0
    }
    __svg_attrs__ = {
        'center':Point
    }

    def __init__(self, center, radius, style=None):
        """
        Initializes.
        """
        super().__init__(center=center, style=style)
        self.radius = radius
        #short-cuts
        self.r = self.radius

    #short-cuts

    @def cx():
        doc = "The cx property."
        def fget(self):
            return self.center.x
        return locals()
    cx = property(**cx())

    @def cy():
        doc = "The cy property."
        def fget(self):
            return self.center.y
        return locals()
    cy = property(**cy())
