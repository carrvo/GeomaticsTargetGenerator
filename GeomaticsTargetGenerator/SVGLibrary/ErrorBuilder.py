"""
This module holds all non-dynamically created error types.
"""

from .__magic__ import name

class TagError(NameError):
    """
    """

    def __init__(self, tag, proper):
        """
        Initializes.
        """
        self.tag = tag
        self.__proper__ = proper

    def __str__(self):
        return 'Tag is not a "{}" it is a "{}"'.format(tagname(self.__proper__), self.tag.name)
    __str__.__doc__ = object.__str__.__doc__

class ParameterError(TypeError):
    """
    Builds custom TypeErrors.
    """

    __type__ = ''

    def __init__(self, false_parameter):
        """
        Initializes.
        """
        self.__parameter__ = false_parameter

    @def parameter():
        doc = "The parameter property."
        def fget(self):
            return self.__parameter__
        return locals()
    parameter = property(**parameter())

    def __str__(self):
        return 'Value {} is not of type {} instead is type {}'.format(self.parameter, name(self.__class__.__type__.__class__), type(self.parameter))
    __str__.__doc__ = object.__str__.__doc__

    @staticmethod
    def CreateError(cls):
        """
        Creates a subclass named by appending 'Error' to cls name.
        Also includes a short-cut to the parameter property
            named by cls name in lowercase.
        """
        clsname = name(cls.__class__)
        class TempError(ParameterError):
            pass
        TempError.__name__ = clsname + 'Error'
        setattr(TempError, clsname.lower(), TempError.parameter)
        setattr(TempError, '__type__', cls)
        return TempError
