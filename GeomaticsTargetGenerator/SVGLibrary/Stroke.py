"""
"""

from collections import Iterable # nicer than checking for '__iter__' -- but str is True for both

from .BaseSVG import AttributeSupport

class Stroke(AttributeSupport):
    """


    linecap examples: butt, round, square
    """

    __svg_to_tag__ = {
        'colour':'stroke',
        'thickness':'stroke-width',
        'linecap':'stroke-linecap',
        'dashes':'stroke-dasharray'
    }

    def __init__(self, colour="black", thickness=1, linecap="square", dashes=(,)):
        """
        Initializes.
        """
        self.colour = colour
        self.thickness = thickness
        self.linecap = linecap
        self.dashes = []

    @staticmethod
    def Attribute(name, value=None):
        """
        Converts an Attribute to an XML Attribute string.
        """
        if value:
            return '{}="{}"'.format(name, value)
        else:
            return ''

    @classmethod
    def ReverseAttribute(cls, name):
        """
        Reverse calculates the svg attribute name from the XML attribute name.
        """
        for svg, tag in cls.__svg_to_tag__.items():
            if tag == name:
                return svg
        raise NameError('Name {} not found.'.format(name))

    # could be separate attributes in the future
    def __xml_repr__(self):
        return ';'.join((
                         self.Attribute(tag, getattr(self, svg))
                         for svg, tag in self.__svg_to_tag__.items()
                         if not isinstance(svg, Iterable) or isinstance(svg, str) # more general
                         else self.Attribute(tag, ','.join((getattr(self, svg))))
                        ))
    __xml_repr__.__doc__ = AttributeSupport.__xml_repr__.__doc__

    # could be separate attributes in the future
    @classmethod
    def __xml_eval__(cls, string):
        string = string.split(';')
        obj = cls()
        for name, value in (s.split('=') for s in string):
            try:
                name = cls.ReverseAttribute(name)
                value = int(value) if value.isnumeric() else value
                if value.find(',') > -1:
                    value = (int(v) for v in value.split(',') if v.isnumeric() else v)
                setattr(obj, name, value)
            except NameError:
                continue # log/print this?
        return obj
    __xml_eval__.__doc__ = AttributeSupport.__xml_eval__.__doc__
