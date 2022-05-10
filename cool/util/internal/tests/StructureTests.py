import unittest

from util.Klass import Klass
from util.KlassRegistry import getKlassByString
from util.Method import Method
from util.internal.HierarchyException import HierarchyException


class StructureTests(unittest.TestCase):
    def setUp(self):
        Klass("Object", None)
        self.k = [Klass("A"), Klass("B", "A"), Klass("C", "B"), Klass("Z", "B")]

    def test1(self):
        self.k[0].addAttribute("a", "Integer")
        self.assertTrue(self.k[0].lookupAttribute("a") == "Integer")

    # Búsqueda por herencia
    def test2(self):
        self.k[0].addAttribute("a", "Integer")
        self.assertTrue(self.k[1].lookupAttribute("a") == "Integer")
        self.assertTrue(self.k[2].lookupAttribute("a") == "Integer")
        self.k[1].addAttribute("b", "String")
        self.assertTrue(self.k[2].lookupAttribute("b") == "String")

    def test3(self):
        with self.assertRaises(KeyError):
            self.k[3].lookupAttribute("z")

    def test4(self):
        m1 = Method("Integer")
        m2 = Method("String", [("a", "Integer"), ("b", "Boolean")])
        self.k[0].addMethod("test", m1)
        self.k[1].addMethod("test2", m2)
        self.assertTrue(self.k[0].lookupMethod("test") == m1)
        self.assertTrue(self.k[2].lookupMethod("test") == m1)
        self.assertTrue(self.k[1].lookupMethod("test2") == m2)

    def test5(self):
        with self.assertRaises(HierarchyException):
            z = Klass("A", "C")

    def test6(self):
        self.assertTrue(getKlassByString("A") == self.k[0])

    def test7(self):
        self.assertTrue(self.k[0].conforms(self.k[2]))
        self.assertFalse(self.k[2].conforms(self.k[1]))
