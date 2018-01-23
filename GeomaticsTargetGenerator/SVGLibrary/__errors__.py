"""
Module short-cut for all Error types.
"""

from .ErrorBuilder import TagError, ParameterError
from .Path import CommandError

#dynamic errors
from .Pair import Pair.__error__ as PairError
from .Pair import Point.__error__ as PointError
from .Style import Style.__error__ as StyleError
from .Path import PathSegment.__error__ as PathSegmentError
