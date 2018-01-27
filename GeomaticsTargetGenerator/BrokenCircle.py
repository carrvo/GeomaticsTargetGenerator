"""
This module provides an extension class to the SVGLibrary
    for ease of TargetDefinition to SVG conversion.
"""

import math

from .SVGLibrary import Circle, Path, PathCommand

from .TargetDefinition import BarCode

class BrokenRing(Path, Circle):
    """
    Extension to SVGLibrary for TargetDefinition conversion.

    It is implemented as a Path but looks like a Circle.
    NOTE: This replaces the Path class for internal lookups.
    """

    def __init__(self, center, radius, angles, angular_units='radians', style=None):
        """
        Initializes.
        """
        if style:
            style.fill = None # https://stackoverflow.com/questions/10213155/unclosed-svg-path-appears-to-be-closed
        self.__class__.__svg_attrs__ = Path.__svg_attrs__
        super(Path, self).__thisclass__.__init__(self) # initial values after
        self.__class__.__svg_attrs__ = Circle.__svg_attrs__
        super(Circle, self).__thisclass__.__init__(self, center, radius, style)
        self.__class__.__svg_attrs__ = Path.__svg_attrs__
        self.replaceWithAngles(angles, angular_units=angular_units)

    @staticmethod
    def polarToCartesian(centerX, centerY, radius, angle, angular_units='degrees'):
        """
        0 is Cartesian +x axis (right of center)

        https://stackoverflow.com/questions/5736398/how-to-calculate-the-svg-path-for-an-arc-of-a-circle
        https://stackoverflow.com/questions/29864022/drawing-parts-of-circles-circumference-in-svg
        """
        if angular_units == 'degrees':
            angleInRadians = (angleInDegrees - 90) * math.pi / 180.0
        else: # angular_units == 'radians'
            angleInRadians = angle
        return {
            'x' : centerX + (radius * math.cos(angleInRadians)),
            'y' : centerY + (radius * math.sin(angleInRadians))
        }

    @staticmethod
    def describeArc(x, y, radius, startAngle, endAngle, angular_units='degrees'):
        """
        https://stackoverflow.com/questions/5736398/how-to-calculate-the-svg-path-for-an-arc-of-a-circle
        https://stackoverflow.com/questions/29864022/drawing-parts-of-circles-circumference-in-svg

        https://www.w3.org/TR/SVG2/paths.html#PathDataEllipticalArcCommands
        a<radiusX>,<radiusY> 0 <bool=0shortArc/1longArc>,<bool=directionOfArc> <moveToX(relativeToCurrent)>,<moveToY(relativeToCurrent)>
        """
        start = BrokenRing.polarToCartesian(x, y, radius, startAngle, angular_units=angular_units)
        end = BrokenRing.polarToCartesian(x, y, radius, endAngle, angular_units=angular_units)
        end = { # cartesian to relative from start
            'x':end['x'] - start['x'],
            'y':-(end['y'] - start['y']) # SVG has positive going down, cartesian has positive going up
        }
        if angular_units == 'degrees':
            largeArcFlag =  "0" if endAngle - startAngle <= 180 else "1"
        else: # angular_units == 'radians'
            largeArcFlag =  "0" if endAngle - startAngle <= math.pi else "1"
        return ( # immutable
            PathCommand.MoveTo(start['x'], start['y'], isabsolute=True),
            PathCommand.EllipticalArcTo(radius, radius, 0, largeArcFlag, 0, end['x'], end['y'], isabsolute=False)
        )

    def convertToArc(self, startAngle, endAngle, angular_units='radians'):
        """
        Extends the static method describeArc with internal variables.
        """
        return self.describeArc(float(self.center.x), float(self.center.y), float(self.radius()), startAngle, endAngle, angular_units=angular_units)

    def addArc(self, startAngle, endAngle, angular_units='radians'):
        """
        convertToArc + addSegment
        """
        arc = self.convertToArc(startAngle, endAngle, angular_units=angular_units)
        self.addSegment(arc[0])
        self.addSegment(arc[1])

    def replaceWithAngles(self, angles, angular_units='radians'):
        """
        angles to arcs
        """
        if (angular_units == 'radians' and not sum(angles) == 2 * math.pi) or (angular_units == 'degrees' and not sum(angles) == 360):
            raise ValueError("Must have total angles be a full circle.")
        self.segments = []
        angles = [0] + list(angles) # safe for list conversion
        current_angle = 0
        for index in range(0, 2, len(angles)):
            current_angle += angles[index]
            self.addArc(current_angle, current_angle + angles[index + 1], angular_units=angular_units)
            current_angle += angles[index + 1]
