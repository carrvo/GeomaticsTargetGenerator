"""
"""

from .BaseSVG import BaseSVG
from .Group import Container
from .Pair import Point
from .__magic__ import xmlrepr, name

class TSpan(BaseSVG):
    """
    Inside Text.
    """

    __tag_name__ = 'tspan'
    __tag_attrs__ = {
        'x':0,
        'y':0
    }
    __svg_attrs__ = {
        'position':Point
    }

    def __init__(self, position, text):
        super(BaseSVG, self).__thisclass__.__init__(self, position=position)
        self.text = text

    #short-cuts

    def x():
        doc = "The x property."
        def fget(self):
            return self.position.x
        def fset(self, value):
            self.position = Point(value, self.y)
        return locals()
    x = property(**x())

    def y():
        doc = "The y property."
        def fget(self):
            return self.position.y
        def fset(self, value):
            self.position = Point(self.x, value)
        return locals()
    y = property(**y())

    def __xml_repr__(self, new_tag):
        tag = xmlrepr(super(BaseSVG, self).__thisclass__, self, new_tag)
        tag.string = str(self.text)
        return tag
    __xml_repr__.__doc__ = BaseSVG.__xml_repr__.__doc__

    @classmethod
    def __xml_eval__(cls, tag):
        if tag.name != tagname(cls):
            raise TagError(tag, cls)
        return cls(*(tag.get(attr, default) for attr, default in tag_attrs(cls).items()), tag.string)
    __xml_eval__.__doc__ = BaseSVG.__xml_eval__.__doc__

class Text(Container, TSpan): #favours Container
    """
    """

    __tag_name__ = 'text'
    __list_type__ = TSpan

    def __init__(self, position, text, subtexts=[]):
        """
        Initializes.
        """
        super(TSPan, self).__init__(position, text)
        super(Container, self).__init__(subtexts)

    def subtexts():
        doc = "The subtexts property."
        def fget(self):
            return self.elements
        def fset(self, value):
            self.elements = value
        return locals()
    subtexts = property(**subtexts())
