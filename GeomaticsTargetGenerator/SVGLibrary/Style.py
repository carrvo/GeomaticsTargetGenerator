"""
"""

from .Stroke import Stroke
from .ErrorBuilder import ParameterError

class Style(Stroke):
    """
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes.
        """
        #should be super(Stroke, self).__init__(*args, **kwargs) but does not work for some reason
        super(Stroke, self).__thisclass__.__init__(self, *args, **kwargs)

    def __xml_repr__(self, tag):
        """
        Sets the 'style' attribute of tag.
        May, in the future, set each
            item in the style attribute
            as individual attributes instead.
        """
        attrstr = ''
        for cls in self.__mro__[1:]: # only superclasses
            # MUST BE CAREFUL OF THIS WHEN SUBCLASSING MORE THAN ONE
            attrstr = ';'.join((attrstr, xmlrepr(super(cls, self))))
        tag['style'] = attrstr
        return tag

    def __xml_eval__(self, tag):
        """
        Recovers object from 'style' attribute of tag.
        May, in the future, recover from multiple
            individual attributes instead.
        """
        # NEEDS TO BE CHANGED TO SUPPORT MULTIPLE SUBCLASSING
        xmleval(super(Stroke, self), tag['style'])
setattr(Style, '__error__', ParameterError.CreateError(Style))
