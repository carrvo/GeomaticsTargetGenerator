"""
"""

from collections import Iterable # nicer than checking for '__iter__' -- but str is True for both

from .AttributeSupport import AttributeSupport

class Stroke(AttributeSupport):
    """


    linecap examples: butt, round, square
    """

    __svg_to_tag__ = {
        'outline':'stroke',
        'thickness':'stroke-width',
        'linecap':'stroke-linecap',
        'dashes':'stroke-dasharray'
    }

    def __init__(self, *args, outline="black", thickness=1, linecap="square", dashes=tuple(), **kwargs):
        """
        Initializes.
        """
        self.outline = outline
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

    # separates attributes
    def __xml_repr__(self, tag): # def __xml_repr__(self):
        # attrs = []
        for svg, attr in self.__svg_to_tag__.items():
            attribute = getattr(self, svg)
            if not isinstance(attribute, Iterable) or isinstance(attribute, str): # more general
                tag[attr] = attribute # attrs.append(self.Attribute(attr, attribute))

            else:
                tag[attr] = ','.join(attribute) # attrs.append(self.Attribute(attr, ','.join(attribute)))
        return tag # return ';'.join(attrs)
    __xml_repr__.__doc__ = AttributeSupport.__xml_repr__.__doc__

    # separate attributes
    @staticmethod # @classmethod
    # static methods act the same as class methods but do not pass in the class so is viable override
    def __xml_eval__(tag): # def __xml_eval__(cls, string):
        return Stroke(**{svg:tag[attr] for svg, attr in Stroke.__svg_to_tag__.items() if tag.get(attr, None)})
        '''
        string = string.split(';')
        obj = cls()
        for name, value in (s.split('=') for s in string):
            try:
                name = cls.ReverseAttribute(name)
                value = int(value) if value.isnumeric() else value
                if value.find(',') > -1:
                    value = (int(v) if v.isnumeric() else v for v in value.split(','))
                setattr(obj, name, value)
            except NameError:
                continue # log/print this?
        return obj
        '''
    __xml_eval__.__doc__ = AttributeSupport.__xml_eval__.__doc__
