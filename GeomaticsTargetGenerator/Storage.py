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
        Returns the full path and file name.
        """
        location = '\\'.join([TargetFile.TargetDirectory(), self.filename])
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
        return {
            name.split('.')[0]
            for name in os.listdir(target_directory)
            if os.path.isfile(os.path.join(target_directory, name))
        }

    def LoadTargetDefinition(self, NotFoundMaxRadius=None):
        """
        Loads a TargetDefinition from a {} file.
        """.format(TargetFile.TDEF)
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
        Saves a TargetDefinition to a {} file.
        """.format(TargetFile.TDEF)
        filename = self.name(TargetFile.TDEF)
        soup = targetdefinition.ToXml()
        with open(filename, mode='wt', encoding='utf-8') as file:
            file.write(soup.prettify())
            file.write('\n') #EOF

    def LoadPreview(self):
        """
        Loads a TargetDefinition from a {} file.
        """.format(TargetFile.VECTOR_IMAGE)
        filename = self.name(TargetFile.VECTOR_IMAGE)
        with open(filename, mode='rb') as file:
            preview = file.read()
        return PreviewData(preview)

    def SavePreview(self, targetdefinition):
        """
        Saves a TargetDefinition to a {} file.
        """.format(TargetFile.VECTOR_IMAGE)
        filename = self.name(TargetFile.VECTOR_IMAGE)
        preview = Previewable(targetdefinition)
        with open(filename, mode='wb') as file:
            file.write(preview)

    def SaveForPrint(self, targetdefinition):
        """
        Saves a TargetDefinition to a {} file.
        """.format(TargetFile.RASTER_IMAGE)
        filename = self.name(TargetFile.RASTER_IMAGE)
        preview = Previewable(targetdefinition)
        printing = Printable(preview)
        with open(filename, mode='wb') as file:
            file.write(printing)

    def ConvertToPrint(self):
        """
        Converts a {} file to a {} file.
        """.format(TargetFile.VECTOR_IMAGE, TargetFile.RASTER_IMAGE)
        filename = self.name(TargetFile.VECTOR_IMAGE)
        with open(filename, mode='rb') as file:
            preview = file.read()
        filename = self.name(TargetFile.RASTER_IMAGE)
        printing = Printable(preview)
        with open(filename, mode='wb') as file:
            file.write(printing)

    def Remove(self):
        """
        Removes all files associated with this TargetFile.
        """
        for ext in [TargetFile.TDEF, TargetFile.VECTOR_IMAGE, TargetFile.RASTER_IMAGE]:
            try:
                os.remove(self.name(ext))
            except FileNotFoundError:
                pass
