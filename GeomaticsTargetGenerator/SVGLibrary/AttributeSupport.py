"""
"""

from .ErrorBuilder import ParameterError

class AttributeSupport(object):
    """
    This provides support for tag attributes.
    """
    __error__ = ParameterError

    def __xml_repr__(self):
        """
        Converts object to string for Tag Attributes.
        """
        raise NotImplementedError('Must override this method!')

    @classmethod
    def __xml_eval__(cls, string):
        """
        Recreate object from a string originating from Tag Attributes.
        """
        raise NotImplementedError('Must override this method!')

class NoAttribute(AttributeSupport): # Should AttributeSupport act in this manner instead?
    """
    This provides a way for an Attribute to be absent.
    """

    def __init__(self):
        """
        Prevents subclassing.
        """
        if not isinstance(self, NoAttribute):
            raise NotImplementedError('{} is not allowed to subclass {}!'.format(self.__class__, NoAttribute))

    def __xml_repr__(self, *args, **kwargs):
        return ''
    __xml_repr__.__doc__ = AttributeSupport.__xml_repr__.__doc__

    @classmethod
    def __xml_eval__(cls, string, *args, **kwargs):
        return NoAttribute()
