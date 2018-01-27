"""
"""

from bs4 import BeautifulSoup

from .BaseSVG import BaseSVG
from .Group import Container
from .__magic__ import xmlrepr, xmleval, tag_attrs

class SVG(Container, BaseSVG): #favours Container
    """
    """

    __tag_name__ = 'svg'
    __tag_attrs__ = {
        'width':100,
        'height':100,
        'xmlns':"http://www.w3.org/2000/svg",
        'version':"1.1"
    }
    __svg_attrs__ = {}

    def __init__(self, width, height):
        """
        Initializes.
        """
        #should be super(Container, self).__init__(elements=[]) but does not work for some reason
        super(Container, self).__thisclass__.__init__(self, elements=[])
        super(BaseSVG, self).__thisclass__.__init__(self)
        self.xmlns = tag_attrs(self.__class__)['xmlns'] ##Until default supported
        self.version = tag_attrs(self.__class__)['version'] ##Until default supported
        self.width = width
        self.height = height

    def __xml_repr__(self, htmlembedded=False):
        """
        Converts object to soup.
        """
        if htmlembedded:
            soup = BeautifulSoup('', 'lxml')
        else:
            soup = BeautifulSoup('', 'xml')
        soup.append(xmlrepr(super(Container, self).__thisclass__, self, soup.new_tag))
        return soup

    @classmethod
    def __xml_eval__(cls, soup):
        """
        Recreate object from soup.
        """
        return xmleval(super(Container, self), soup.svg)
