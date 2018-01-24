"""
Module short-cut for all Error types.
"""

from .ErrorBuilder import TagError, ParameterError
from .Path import CommandError

#dynamic errors
from .Pair import Pair
PairError = Pair.__error__
from .Pair import Point
PointError = Point.__error__
from .Style import Style
StyleError = Style.__error__
from .Path import PathSegment
PathSegmentError = PathSegment.__error__

_locals = locals()

__all__ = [ local for local in _locals if local.endswith('Error') ]
