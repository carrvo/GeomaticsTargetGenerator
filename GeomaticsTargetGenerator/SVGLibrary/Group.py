"""
"""

from .BaseSVG import BaseSVG
from .__magic__ import xmlrepr, xmleval, name, check

class Container(object):
    """
    """

    __list_type__ = BaseSVG

    def __init__(self, elements=[]):
        """
        Initializes.
        """
        self.elements = elements

    def __xml_repr__(self, new_tag):
        tag = xmlrepr(super(self.__class__.__mro__[2], self).__thisclass__, self, new_tag) #assumes self.__mro__[1] == Container
        for element in self.elements:
            tag.append(xmlrepr(element, new_tag))
        return tag
    __xml_repr__.__doc__ = BaseSVG.__xml_repr__.__doc__

    @classmethod
    def __xml_eval__(cls, tag):
        group = xmleval(super(cls.__mro__[2], self), tag) #assumes cls.__mro__[1] == Container
        group.elements = [xmleval(cls.__list_type__, element) for element in tag.children]
        return group
    __xml_eval__.__doc__ = BaseSVG.__xml_eval__.__doc__

class Group(Container, BaseSVG): #favours Container
    """
    """

    __tag_name__ = 'g'
    __tag_attrs__ = {
        'id':''
    }
    __svg_attrs__ = {}

    def __init__(self, id, elements=[]):
        """
        Initializes.
        """
        super(Container, self).__init__(elements)
        super(BaseSVG, self).__init__(id=id)

class Hyperlink(BaseSVG):
    """
    """

    __tag_name__ = 'a'
    __tag_attrs__ = {
        'xlink:href':'',
        'target':'_blank'
    }
    __svg_attrs__ = {
        'url':str
    }
    __type__ = BaseSVG

    def __init__(self, url, wrapped):
        """
        Initializes.
        """
        super(BaseSVG, self).__thisclass__.__init__(self, url=url)
        if not isinstance(wrapped, self.__class__.__type__):
            raise TypeError()##
        self.wrapped = wrapped

    def __xml_repr__(self, new_tag):
        tag = xmlrepr(super(BaseSVG, self).__thisclass__, self, new_tag)
        tag.append(xmlrepr(self.wrapped, new_tag))
        return tag
    __xml_repr__.__doc__ = BaseSVG.__xml_repr__.__doc__

    @classmethod
    def __xml_eval__(cls, tag):
        hyper = xmleval(super(BaseSVG, self), tag)
        hyper.wrapped = xmleval(cls.__type__, tag.children[0])
        return hyper
    __xml_eval__.__doc__ = BaseSVG.__xml_eval__.__doc__
