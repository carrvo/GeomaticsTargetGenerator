"""

NOTE: asserts to be replaced with other Error Types.
"""

import math

from bs4 import BeautifulSoup

class BarCode(object):
    """
    """

    def __init__(self, inner_radius, outer_radius, angles):
        """
        Initializes.
        """
        assert 0 < inner_radius < 100, "Cannot be negative or exceed 100%."
        assert 0 < outer_radius <= 100, "Cannot be negative or exceed 100%."
        assert outer_radius > inner_radius, "Must have radii increase."
        self.InnerRadius = inner_radius
        self.OuterRadius = outer_radius
        assert sum(angles) == 2 * math.pi, "Must have total angles be a full circle."
        self.Angles = angles

    def Width(self):
        """
        Radial width of BarCode.
        """
        return self.OuterRadius - self.InnerRadius

class TargetDefinition(object):
    """
    """

    def __init__(self, max_radius):
        """
        Initializes.
        """
        self.Cocentric = [] #Ordered Towards Outside
        self.MaxRadius = max_radius
        self.ColouredCircles #Name to be changed

    def Add(ring):
        """
        """
        assert isinstance(ring, BarCode), "Currently only support adding BarCode Instances"
        if self.Cocentric: #If not empty
            assert ring.InnerRadius > self.Cocentric[-1].OuterRadius, "Must be ordered towards the outside."
            assert ring.Width > self.Cocentric[-1].Width(), "Must have width increase."
        self.Cocentric.Add(ring)

    def AddColouredCircle(ColouredCircle):
        """
        """
        pass #TODO

    @staticmethod
    def FromXml(soup):
        """
        Converts a BeautifulSoup XML format to a TargetDefinition.
        """
        pass #TODO

    def ToXml():
        """
        Converts TargetDefinition to a BeautifulSoup XML format.
        """
        pass #TODO
