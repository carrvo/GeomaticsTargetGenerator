"""
This module is for dealing with the filesystem.
"""

from bs4 import BeautifulSoup

from .TargetDefinition import TargetDefinition
from .Images import Previewable, Printable, PreviewData

PARSER = "xml"

class TargetFile(object):
    """
    This class is for accessing the various used file types.
    """

    #File Types
    TDEF = 'tdef'
    VECTOR_IMAGE = '' #TODO
    RASTER_IMAGE = '' #TODO

    STORAGE_LOCATION = 'TargetDefinitions'

    def __init__(self, filename):
        """
        Initialization.
        """
        self.filename = filename

    def name(self, filetype):
        """
        """
        location = '\\'.join([TargetFile.STORAGE_LOCATION, self.filename])
        return '.'.join([location, filetype])

    def LoadTargetDefinition(self):
        """
        """
        filename = self.name(TargetFile.TDEF)
        with open(filename, mode='rt', encoding='utf-8') as file:
            tdef = file.read()
        soup = BeautifulSoup(tdef, PARSER)
        return TargetDefinition.FromXml(soup)

    def SaveTargetDefinition(self, targetdefinition):
        """
        """
        filename = self.name(TargetFile.TDEF)
        soup = targetdefinition.ToXml()
        with open(filename, mode='wt', encoding='utf-8') as file:
            file.write(soup.prettify())
            file.write('\n') #EOF

    def LoadPreview(self):
        """
        """
        filename = self.name(TargetFile.VECTOR_IMAGE)
        with open(filename, mode='rb') as file:
            preview = file.read() #TODO
        return PreviewData(preview)

    def SavePreview(self, targetdefinition):
        """
        """
        filename = self.name(TargetFile.VECTOR_IMAGE)
        preview = Previewable(targetdefinition)
        with open(filename, mode='wb') as file:
            file.write(preview)

    def SaveForPrint(self, targetdefinition):
        """
        """
        filename = self.name(TargetFile.RASTER_IMAGE)
        preview = Previewable(targetdefinition)
        printing = Printable(preview)
        with open(filename, mode='wb') as file:
            file.write(printing)

    def ConvertToPrint(self):
        """
        """
        filename = self.name(TargetFile.VECTOR_IMAGE)
        with open(filename, mode='rb') as file:
            preview = file.read() #TODO
        filename = self.name(RASTER_IMAGE)
        printing = Printable(preview)
        with open(filename, mode='wb') as file:
            file.write(printing)
