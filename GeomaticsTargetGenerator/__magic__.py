"""
This module specifies custom magic methods.
"""

def crepr(obj, *args, **kwargs):
    """
    Machine representation of object.
    Used to recreate object.
    """
    return obj._c__repr__(*args, **kwargs)

def ceval(cls, *args, **kwargs):
    """
    Recreates object through static method.
    """
    return cls._c__eval__(*args, **kwargs)
