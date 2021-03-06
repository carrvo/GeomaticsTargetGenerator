"""
"""

from .AttributeSupport import AttributeSupport
from .Stroke import Stroke
from .ErrorBuilder import ParameterError
from .__magic__ import xmlrepr

class Style(Stroke):
    """
    """

    __svg_to_tag__ = {'fill':'fill'}
    __svg_to_tag__.update(Stroke.__svg_to_tag__)

    def __init__(self, *args, colour=None, **kwargs):
        """
        Initializes.
        """
        #should be super(Stroke, self).__init__(*args, **kwargs) but does not work for some reason
        super(Stroke, self).__thisclass__.__init__(self, *args, **kwargs)
        self.fill = colour

    def __xml_repr__(self, tag):
        """
        Sets the style-related attributes of tag.
        """
        for cls in [cls for cls in self.__class__.__mro__ if cls != self.__class__ and cls != AttributeSupport and cls != object]: # only superclasses
            xmlrepr(super(cls, self).__thisclass__, self, tag)
        tag['fill'] = str(self.fill)
        return tag
        """
        Sets the 'style' attribute of tag.
        May, in the future, set each
            item in the style attribute
            as individual attributes instead.
        """
        '''
        attrstr = ''
        for cls in [cls for cls in self.__class__.__mro__ if cls != self.__class__ and cls != AttributeSupport and cls != object]: # only superclasses
            # MUST BE CAREFUL OF THIS WHEN SUBCLASSING MORE THAN ONE
            klass = super(cls, self).__thisclass__
            attrstr = ';'.join((attrstr, xmlrepr(klass, self)))
        tag['fill'] = str(self.fill)
        tag['style'] = attrstr
        return tag
        '''

    @classmethod
    def __xml_eval__(cls, tag):
        """
        Recovers object from multiple individual attributes.
        """
        return cls(**{svg:tag[attr] for svg, attr in cls.__svg_to_tag__.items() if tag.get(attr, None)})
        """
        Recovers object from 'style' attribute of tag.
        May, in the future, recover from multiple
            individual attributes instead.
        """
        '''
        # NEEDS TO BE CHANGED TO SUPPORT MULTIPLE SUBCLASSING
        obj = xmleval(super(Stroke, self), tag['style'])
        obj.fill = tag['fill']
        return obj
        '''
setattr(Style, '__error__', ParameterError.CreateError(Style))
