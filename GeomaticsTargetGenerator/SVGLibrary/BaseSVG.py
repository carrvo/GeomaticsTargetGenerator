"""
"""

from .Style import Style
from .AttributeSupport import NoAttribute
from .__magic__ import xmlrepr, xmleval, name, tagname, tag_attrs, check
from .TagError import TagError

class Register(type):
    def __init__(cls, name, bases, namespace):
        super(Register, cls).__init__(name, bases, namespace)
        if not hasattr(cls, '__registry__'):
            cls.__registry__ = {}
        cls.__registry__.update({tagname(cls):cls})
    # Metamethods, called on class objects:
    def __getitem__(cls, key):
        return cls.__registry__[key]

class BaseSVG(object, metaclass=Register):
    """
    This is the class for which all SVG tag classes inherit.

    Rapid Building Requirements:
        - class have __name__ for SVG tag name
        - class have __tag_attrs__ for SVG tag attributes
            (excludes style or style attributes)
            --> { 'name':default }
        - class have a field/property for every
            value in __tag_attrs__
        - class have __svg_attrs__ for SVG class properties
            and parameters (excludes style or style attributes).
            --> { 'name':type }
            --> if not included then must be manually coded
        - in __init__ call super(..., self).__thisclass__.__init__(self, ...)
            with parameters in __svg_attrs__
            --> do not need to include all parameters
            --> note that if __svg_attrs__ type does
                    not have a __default__ method then
                    will initialize with NoneType
    """

    __tag_name__ = ''
    __tag_attrs__ = {} #'name':default
    __svg_attrs__ = {} #'name':type

    def __init__(self, **kwargs):
        """
        Initializes.
        """
        for attr, _type in self.__class__.__svg_attrs__.items():
            try:
                setattr(self, '_' + attr, check(_type, kwargs[attr]))
            except IndexError:
                setattr(self, '_' + attr, default(_type))
            except _type.__error__ as error:
                error.args += (attr,)
                raise error
        try:
            self.__style__ = check(Style, kwargs.get('style', None))
        except Style.__error__:
            self.__style__ = NoAttribute()
        self.set_properties()

    @classmethod
    def set_properties(cls):
        """
        Sets the properties according to __svg_attrs__
            making sure to type check.
        """
        for attr, _type in cls.__svg_attrs__.items():
            def temp():
                doc = "The {} property.".format(attr)
                def fget(self):
                    return getattr(self, '_' + attr)
                def fset(self, value):
                    setattr(self, '_' + attr, check(_type, value))
                local = locals()
                local.pop('attr')
                local.pop('_type')
                return local
            temp = property(**temp())
            setattr(cls, attr, temp)

    def style():
        doc = "The style property."
        def fget(self):
            return self.__style__
        def fset(self, value):
            check(Style, value)
            self.__style__ = value
        def fdel(self):
            self.__style__ = NoAttribute() ##
        return locals()
    style = property(**style())

    def __xml_repr__(self, new_tag):
        """
        Converts object to Tag object in soup.
        """
        tag = new_tag(tagname(self.__class__))
        for attr in tag_attrs(self.__class__).keys():
            tag[attr] = getattr(self, attr) ##TODO: support default
        #tag['style'] = repr(self.style)
        xmlrepr(self.style, tag)
        return tag

    @classmethod
    def __xml_eval__(cls, tag):
        """
        Recreate object from Tag object in a soup.
        """
        if cls == __class__:
            klass = __class__[tag.name] # this class can generate any others
        else: # however subclasses can only generate themselves
            if tag.name != tagname(cls):
                raise TagError(tag, cls)
            klass = cls
        return klass(*(tag.get(attr, default) for attr, default in tag_attrs(klass).items()), style=xmleval(Style, tag))
