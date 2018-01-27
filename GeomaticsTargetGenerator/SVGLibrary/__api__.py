"""
This module specifies the API.
"""

#SVG Classes
from .Circle import Circle
from .Ellipse import Ellipse
from .Group import Group, Hyperlink
from .Line import Line
from .Path import Path
from .Poly import Polyline, Polygon
from .Rectangle import Rectangle
from .Text import TSpan, Text

#Main SVG class
from .SVG import SVG

#Support Classes
from .AttributeSupport import NoAttribute
from .Style import Style
from .Pair import Pair, Point
#Path Commands
'''
from .Path import MoveTo, LineTo
from .Path import HorizontalLineTo, VerticalLineTo
from .Path import CurveTo, SmoothCurveTo
from .Path import QuadraticBezierCurveTo
from .Path import SmoothQuadraticBezierCurveTo
from .Path import EllipticalArcTo, ClosePath
'''
from .Path import PathCommand # use them as methods instead

#Errors
from . import __errors__ as Errors

#Utility functions
from .__magic__ import xmlrepr, xmleval

API_DOC = """
"""

class API(object):
    """
    This class is a facade that wraps all of the functionality into a class.

    {}
    """.format(API_DOC)
    pass
