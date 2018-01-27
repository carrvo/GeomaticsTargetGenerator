"""
"""

from .BaseSVG import BaseSVG
from .Pair import Point
from .__magic__ import xmlrepr, xmleval, tagname, tag_attrs, check

class Polyline(BaseSVG):
    """
    """

    __tag_name__ = 'polyline'
    __tag_attrs__ = {
        'points':[]
    }
    __svg_attrs__ = {}
    __list_type__ = Point

    def __init__(self, points, style=None):
        """
        Initializes.
        """
        super(BaseSVG, self).__thisclass__.__init__(self, style=style)
        self.points = points

    def __xml_repr__(self, new_tag):
        poly = new_tag(tagname(self.__class__))
        poly[tuple(tag_attrs(self).keys())[0]] = ' '.join([xmlrepr(check(self.__class__.__list_type__, point)) for point in self.points])
        xmlrepr(self.style, poly)
        return poly
    __xml_repr__.__doc__ = BaseSVG.__xml_repr__.__doc__

    @classmethod
    def __xml_eval__(cls, tag):
        if tag.name != tagname(cls):
            raise TagError(tag, cls)
        return cls([xmleval(cls.__list_type__, position) for position in tag['points'].split(' ')])
    __xml_eval__.__doc__ = BaseSVG.__xml_eval__.__doc__

class Polygon(Polyline):
    """
    """
    __tag_name__ = 'polygon'
