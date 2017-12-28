"""
Module for testing the loading, modifying, and storing of the *.tdef files.
This includes both API and Console testing.
"""

import os
import unittest
from io import StringIO

try:
    from GeomaticsTargetGenerator import TargetFile, BarCode, TargetDefinition
    from GeomaticsTargetGenerator.Console import Console
except ImportError:
    try:
        from . import context
    except ImportError:
        import context
    from GeomaticsTargetGenerator import TargetFile, BarCode, TargetDefinition
    from GeomaticsTargetGenerator.Console import Console

class TargetDefinitionLifeCycle(unittest.TestCase):
    """
    Monolithic testing of:
        - Creating from blank
        - Modifying existing
        - Deleting existing
    Includes both API and Console (through StringIO) usage.
    """

    @classmethod
    def setUpClass(cls):
        """
        """
        cls.TestFile = 'testing'

    @classmethod
    def tearDownClass(cls):
        """
        """
        directory = TargetFile.TargetDirectory()
        for filename in os.listdir(filename):
            if filename.startswith(cls.TestFile):
                os.remove(os.path.join(directory, filename))

    def setUp(self):
        """
        """
        self.target_file = TargetFile(TargetDefinitionLifeCycle.TestFile)
        self.target_definition = self.target_file.LoadTargetDefinition(100)

    def tearDown(self):
        """
        """
        pass

    def _ssubtests(self):
        for name in sorted(dir(self)):
            if name.startswith("subtest_"):
                yield name, getattr(self, name)

    def test_steps(self):
        for i, name, subtest in enumerate(self._steps()):
            with self.subTest(i=i, name=name):
                subtest()

    def subtest_1(self):
        """
        Tests completed execution of saving a Target.
        """
        self.target_file.SaveTargetDefinition(self.target_definition)
        self.assertTrue(True)

    def subtest_2(self):
        """
        Tests completed execution of loading a Target.
        """
        self.targetdefinition = self.target_file.LoadTargetDefinition()
        self.assertTrue(True)

    def subtest_3(self):
        """
        Tests completed execution of API modification of a Target.
        """
        self.target_definition.ChangeMaxRadius(50)
        barcode = BarCode(5, 10, [360], angular_units='degrees')
        self.target_definition.Add(barcode)
        barcode = BarCode(15, 25, [90,90,90,90], angular_units='degrees')
        self.target_definition.Add(barcode)
        self.assertTrue(True)

    def subtest_4(self):
        """
        Tests completed execution of saving a Target to a different file.
        """
        self.target_file = TargetFile(TargetDefinitionLifeCycle.TestFile + '2')
        self.target_file.SaveTargetDefinition(self.target_definition)
        self.assertTrue(True)

    def subtest_5(self):
        """
        Tests completed execution of Console modification.
        """
        commands = StringIO("""
            load {testfile}2
            load {testfile}3
            addbarcode 40 80 30 60 90 90 60 30 angular_units=degrees
            modify MaxRadius 200
            modify BarCode 1
            outer 30
            angles 30 60 90 90 90 angular_units=degrees
            done
            save Definition
        """.format(testfile=TargetDefinitionLifeCycle.TestFile))
        console = Console(stdin=commands)
        console.cmdLoop()
        self.assertTrue(True)
