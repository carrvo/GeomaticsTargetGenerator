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
