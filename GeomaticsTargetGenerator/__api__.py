"""
This module specifies the API.
"""

from .TargetDefinition import BarCode, TargetDefinition
from .Storage import TargetFile

API_DOC = """
"""

class API(object):
    """
    This class is a facade that wraps all of the functionality into a class.

    {}
    """.format(API_DOC)

    def __init__(self, filename=None):
        """
        Initializes.
        """
        self.current_target_definition = None
        self.current_file = None
        if filename:
            self.load(filename)

    @staticmethod
    def AvailableNames():
        return TargetFile.AvailableNames()
    AvailableNames.__doc__ = TargetFile.AvailableNames.__doc__

    @property
    def current(self):
        """
        Current Target Definition loaded into API.
        """
        return self.current_target_definition

    @property
    def file(self):
        """
        Current File being edited.
        """
        return self.current_file

    def load(self, filename):
        """
        Loads file for current editing.
        If file does not exist then creates a new one.
        """
        self.current_file = TargetFile(filename)
        self.current_target_definition = self.file.LoadTargetDefinition()

    def save(self, option=None):
        """
        Saves the current Definition into the current file.
        Default is to save as Definition file.
        Options: Definition, Prievew (future), Print (future)
        """
        option = option.lower()
        if option == 'preview':
            self.file.SavePreview(self.current)
        elif option == 'print':
            self.file.SaveForPrint(self.current)
        else: #Definition
            self.file.SaveTargetDefinition(self.current)

    def clear(self, option=None):
        """
        Clears current Definition and current file.
        Optional: specify to clear just Definition or file.
        """
        option = option.lower()
        if option == 'definition':
            self.current_target_definition = None
        elif option == 'file':
            self.current_file = None
        else:
            self.current_file = None
            self.current_target_definition = None

    def remove(self):
        self.file.Remove()
    remove.__doc__ = TargetFile.Remove.__doc__

    def modify(self, mod, level=None):
        """
        Returns for Modification:
            - BarCode [+ ring level ordered outward]
                removes and returns list at level and outward
            - MaxRadius [+ new value] - not returned
            - ColouredCircle (future)
        """
        mod = mod.lower()
        if mod == 'barcode':
            return self.current.RemoveFrom(level) #int
        elif mod == 'maxradius':
            self.current.ChangeMaxRadius(level) #float
        elif mod == 'colouredcircle':
            self.current.GetColouredCircle(level) #int
        else:
            raise NameError("{} cannot be modified.".format(mod))

    def addbarcode(self, inner, outer, *args, **kwargs):
        """
        Adds a BarCode to the current Definition.
        API.addbarcode(<inner radius>, <outer radius>, <angle>, [<angle>, [...]] [kwarg=value, [...]])
        """
        self.current.Add(BarCode(inner, outer, args, **kwargs))

    def addbarcodeobject(self, barcode):
        """
        Adds a BarCode to the current Definition.
        For re-adding those removed for modification.
        """
        if not isinstance(barcode, BarCode):
            raise TypeError("{} of type {} must be a BarCode instance".format(str(barcode), type(barcode)))
        self.current.Add(barcode)

    def addcode(self, inner, outer, code):
        """
        Adds a BarCode to the current Definition.
        API.addcode(<inner radius>, <outer radius>, <code>)
        """
        self.current.Add(BarCode(inner, outer, code, coded=True))

    def addcolouredcircle(self, *args, **kwargs):
        """
        (future)
        """
        self.current.AddColouredCircle('TODO') #TODO
