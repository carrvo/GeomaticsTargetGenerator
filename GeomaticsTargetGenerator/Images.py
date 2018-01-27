"""
This module is for creating and printing image files from TargetDefinition.
"""

from bs4 import BeautifulSoup as BS

from .SVGLibrary import *

from .TargetDefinition import TargetDefinition
from .BrokenCircle import BrokenRing, Ring

def Previewable(targetdefinition):
    """
    Converts a TargetDefinition to a Vector Image File to be saved and previewed.
    """
    fill_area = targetdefinition.MaxRadius * 2
    svg = SVG(fill_area, fill_area)
    center = targetdefinition.MaxRadius
    center = Point(center, center)
    for barcode in reversed(targetdefinition.Cocentric):
        #should be percentages of max not absolute
        line = Style(outline="black", thickness=barcode.Width())
        if len(barcode.Angles) == 1: # full circle
            svg.elements.append(Ring(center, barcode.CenterRadius, style=line))
        else:
            svg.elements.append(BrokenRing(center, barcode.CenterRadius, barcode.Angles, angular_units='radians', style=line))
    for circle in targetdefinition.ColouredCircles:
        pass #TODO
    return xmlrepr(svg).prettify()

def Printable(vectorimage):
    """
    Converts a Vector Image File to a Raster Image File for a printer.
    NOTE: this depends on printer properties.
    """
    raise NotImplementedError() #TODO

def PreviewData(vectorimage):
    """
    Converts a Vector Image File to a TargetDefinition
    """
    raise NotImplementedError() #TODO
