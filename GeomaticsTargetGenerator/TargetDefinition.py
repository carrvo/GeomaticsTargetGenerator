"""

NOTE: asserts to be replaced with other Error Types.
"""

import math

from bs4 import BeautifulSoup

PARSER = "xml"#from .Storage import PARSER

class BarCode(object):
    """
    """

    def __init__(self, inner_radius, outer_radius, angles, angular_units='radians', coded=False):
        """
        Initializes.
        if coded then angles is the input code.
        """
        self.ChangeRadii(inner_radius, outer_radius)
        if coded:
            self.ChangeCode(angles)
        else:
            self.ChangeAngles(angles, angular_units=angular_units)

    def Width(self):
        """
        Radial width of BarCode.
        """
        return self.OuterRadius - self.InnerRadius

    def ChangeRadii(self, inner, outer):
        """
        Changes the Inner Radus and Outer Radius.
        """
        assert 0 < inner_radius < 100, "Cannot be negative or exceed 100%."
        assert 0 < outer_radius <= 100, "Cannot be negative or exceed 100%."
        assert outer_radius > inner_radius, "Must have radii increase."
        self.InnerRadius = inner_radius
        self.OuterRadius = outer_radius

    def ChangeAngles(self, angles, angular_units='radians'):
        """
        Changes the angles and performs check that make a full circle.
        """
        if angular_units == 'degrees':
            angles = [angle / 180 * math.pi for angle in angles]
        assert sum(angles) == 2 * math.pi, "Must have total angles be a full circle."
        self.Angles = angles

    def ChangeCode(self, code):
        """
        """
        pass #TODO

    def __repr__(self):
        """
        Machine representation of object.
        """
        super().__repr__() #TODO?

    def __str__(self):
        """
        Human readable representation of object.
        """
        return '''
            InnerRadius: {}
            OuterRadius: {}
            Angles: {}
        '''.format(self.InnerRadius, self.OuterRadius, self.Angles)


class TargetDefinition(object):
    """
    """

    def __init__(self, max_radius):
        """
        Initializes.
        """
        self.Cocentric = [] #Ordered Towards Outside
        self.ChangeMaxRadius(max_radius)
        self.ColouredCircles = [] #Name to be changed

    def ChangeMaxRadius(self, radius):
        """
        """
        assert radius != 0, "Must have a radius."
        self.MaxRadius = radius

    def Add(self, ring):
        """
        Adds the next level of BarCode.
        """
        assert isinstance(ring, BarCode), "Currently only support adding BarCode Instances"
        if self.Cocentric: #If not empty
            assert ring.InnerRadius > self.Cocentric[-1].OuterRadius, "Must be ordered towards the outside."
            assert ring.Width > self.Cocentric[-1].Width(), "Must have width increase."
        self.Cocentric.append(ring)

    def RemoveFrom(self, ring_level):
        """
        Gets the BarCode at ring_level.
        """
        ret = self.Cocentric[ring_level:]
        self.Cocentric[:ring_level]
        return ret

    def AddColouredCircle(self, ColouredCircle):
        """
        """
        pass #TODO

    def GetColouredCircle(self, number):
        """
        """
        return self.ColouredCircles[number]

    def RemoveColouredCircle(self, number):
        """
        """
        del self.ColouredCircles[number]

    @staticmethod
    def FromXml(soup):
        """
        Converts a BeautifulSoup XML format to a TargetDefinition.
        """
        definition = TargetDefinition(float(soup.TargetDefinition['max_radius']))
        for ring in soup.TargetDefinition.BarCodes.find_all("BarCode", recursive=False): #...BarCodes.children but not NavigableString
            #Supports radians and degrees
            angles = [ float(angle.string) if angle['units'] == 'radians' else float(angle.string) / 180 * math.pi for angle in ring.find_all("angle", recursive=False) ] #ring.children but not NavigableString
            definition.Add(BarCode(float(ring['inner_radius']), float(ring['outer_radius']), angles))
        for circle in soup.TargetDefinition.ColouredCircles.find_all("ColouredCircle"):
            pass #definition.AddColouredCircle()
        return definition

    def ToXml(self, angular_units='radians'):
        """
        Converts TargetDefinition to a BeautifulSoup XML format.
        """
        soup = BeautifulSoup("", PARSER)
        new_tag = soup.new_tag
        soup.append(new_tag("TargetDefinition", max_radius=self.MaxRadius))
        soup.TargetDefinition.append(new_tag("BarCodes"))
        for ring in self.Cocentric:
            ring_tag = new_tag("BarCode", inner_radius=ring.InnerRadius, outer_radius=ring.OuterRadius)
            for angle in ring.Angles:
                angle_tag = new_tag("angle", units=angular_units)
                if angular_units == 'radians':
                    angle_tag.string = str(angle)
                else: #degrees
                    angle_tag.string = str(angle / math.pi * 180)
                ring_tag.append(angle_tag)
            soup.TargetDefinition.BarCodes.append(ring_tag)
        soup.TargetDefinition.append(new_tag("ColouredCircles"))
        for circle in self.ColouredCircles:
            pass #
        return soup
