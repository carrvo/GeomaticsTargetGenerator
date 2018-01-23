"""
This module specifies custom magic methods.
"""

def xmlrepr(obj, *args, **kwargs):
    """
    Converts to a BeautifulSoup XML format.
    Used to recreate object.
    """
    return obj.__xml_repr__(new_tag, *args, **kwargs)

def xmleval(cls, *args, **kwargs):
    """
    Converts from a BeautifulSoup XML format.
    Recreates object through static method.
    """
    return cls.__xml_eval__(tag, *args, **kwargs)

def name(obj_cls):
    """
    Retrieves the name set.
    Nicer syntax.
    """
    return obj_cls.__name__

def tagname(obj_cls):
    """
    Retrieves the name set.
    Nicer syntax.
    """
    return obj_cls.__tag_name__

def tag_attrs(cls):
    """
    Retrieves the attributes to be used in the xml tag.
    """
    return cls.__tag_attrs__

def default(cls):
    """
    """
    try:
        return cls.__default__
    except AttributeError:
        return None

def check(cls, obj, *args, **kwargs):
    """
    Checks obj against cls.
    """
    if not isinstance(obj, cls):
        raise cls.__error__(obj, *args, **kwargs)
    return obj
