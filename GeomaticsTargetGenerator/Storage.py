"""
This module is for dealing with the filesystem.
"""

import os

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

    @staticmethod
    def TargetDirectory():
        """
        Gives the absolute path of where the Targets are stored.
        """
        return os.path.abspath(TargetFile.STORAGE_LOCATION)

    @staticmethod
    def AvailableNames():
        """
        Set of all available files.
        """
        target_directory = TargetFile.TargetDirectory()
        return {name.split('.')[0] if os.path.isfile(os.path.join(target_directory, name)) for name in os.listdir(target_directory) }

    def LoadTargetDefinition(self, NotFoundMaxRadius=None):
        """
        """
        try:
            filename = self.name(TargetFile.TDEF)
            with open(filename, mode='rt', encoding='utf-8') as file:
                tdef = file.read()
            soup = BeautifulSoup(tdef, PARSER)
            return TargetDefinition.FromXml(soup)
        except FileNotFoundError:
            print('Not found - New Target Definition will be created')
            if NotFoundMaxRadius:
                radius = NotFoundMaxRadius
            else:
                radius = input('Please enter max radius:')
            return TargetDefinition(radius)

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
