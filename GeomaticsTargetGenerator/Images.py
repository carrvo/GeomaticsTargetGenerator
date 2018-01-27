"""
This module is for creating and printing image files from TargetDefinition.
"""

from bs4 import BeautifulSoup as BS

try:
    from .SVGLibrary import *
except ImportError as error:
    print(error)
    error.with_traceback()

from .TargetDefinition import TargetDefinition

def Previewable(targetdefinition):
    """
    Converts a TargetDefinition to a Vector Image File to be saved and previewed.
    """
    fill_area = targetdefinition.MaxRadius * 2
    svg = SVG(fill_area, fill_area)
    center = targetdefinition.MaxRadius
    center = Point(center, center)
    black = Style(colour="black")
    white = Style(colour="white")
    for barcode in reversed(targetdefinition.Cocentric):
        #should be percentages of max not absolute
        svg.elements.append(Circle(center, barcode.OuterRadius, style=black))
        svg.elements.append(Circle(center, barcode.InnerRadius, style=white))
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
