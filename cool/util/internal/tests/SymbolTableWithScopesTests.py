import unittest

from util.internal.SymbolTable import SymbolTable


class PruebasConTablaLineal(unittest.TestCase):
    # Corre antes de cada método de prueba
    def setUp(self):
        self.st = SymbolTable()

    # Corre después de cada método de prueba
    def tearDown(self):
        self.st = None

    def test1(self):
        self.assertFalse('a' in self.st.keys())

    def test2(self):
        self.st['hola'] = 'mundo1'
        self.assertTrue('hola' in self.st.keys())
        self.assertTrue(self.st['hola'] == 'mundo1')

    def test3(self):
        with self.assertRaises(KeyError):
            a = self.st['hola']

    def test4(self):
        self.st['hola'] = 'mundo'
        with self.assertRaises(KeyError):
            self.st['hola'] = 'mundo'
