"""
This module is for dealing with the filesystem.
"""

from bs4 import BeautifulSoup

from .Storage import TargetDefinition
from .Images import Previewable, Printable, PreviewData

class TargetFile(object):
    """
    This class is for accessing the various used file types.
    """

    TDEF = 'tdef'
    VECTOR_IMAGE = '' #TODO
    RASTER_IMAGE = '' #TODO

    def __init__(self, filename):
        """
        Initialization.
        """
        self.filename = filename

    def name(self, filetype):
        """
        """
        return '.'.join(self.filename, filetype)

    def LoadTargetDefinition(self):
        """
        """
        filename = self.name(TDEF)
        with open(filename, mode='rt', encoding='utf-8') as file:
            tdef = '\n'.join(file.readLines)
        soup = BeautifulSoup(tdef)
        return TargetDefinition.FromXml(soup)

    def SaveTargetDefinition(self, targetdefinition):
        """
        """
        filename = self.name(TDEF)
        with open(filename, mode='wt', encoding='utf-8') as file:
            file.writeLines(targetdefinition.prettify())

    def LoadPreview(self):
        """
        """
        filename = self.name(VECTOR_IMAGE)
        with open(filename, mode='rb') as file:
            preview = file.read() #TODO
        return PreviewData(preview)

    def SavePreview(self, targetdefinition):
        """
        """
        filename = self.name(VECTOR_IMAGE)
        preview = Previewable(targetdefinition)
        with open(filename, mode='wb') as file:
            file.write(preview)

    def SaveForPrint(self, targetdefinition):
        """
        """
        filename = self.name(RASTER_IMAGE)
        preview = Previewable(targetdefinition)
        printing = Printable(preview)
        with open(filename, mode='wb') as file:
            file.write(printing)

    def ConvertToPrint(self):
        """
        """
        filename = self.name(VECTOR_IMAGE)
        with open(filename, mode='rb') as file:
            preview = file.read() #TODO
        filename = self.name(RASTER_IMAGE)
        printing = Printable(preview)
        with open(filename, mode='wb') as file:
            file.write(printing)
