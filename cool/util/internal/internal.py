import unittest

from util.Klass import Klass
from util.internal.SymbolTableWithScopes import SymbolTableWithScopes


class SymbolTableWithScopesTests(unittest.TestCase):
    def setUp(self):
        k = Klass("Object", None)
        self.st = SymbolTableWithScopes(k)

    def tearDown(self):
        self.st = None

    def test1(self):
        self.assertFalse('a' in self.st.keys())

    def test2(self):
        self.st['hola'] = 'mundo1'
        self.assertTrue('hola' in self.st.keys())
        self.assertTrue(self.st['hola'] == 'mundo1')

    def test3(self):
        self.st['hola'] = 'mundo2'
        self.assertTrue('mundo2' in self.st.values())

    def test4(self):
        self.st['hola'] = 'mundo3'
        self.assertEqual('mundo3', self.st['hola'])

    def test5(self):
        with self.assertRaises(KeyError):
            a = self.st['hola']

    def test6(self):
        self.st.openScope()
        self.st['hola'] = 'mundo1'
        self.st.closeScope()
        self.assertFalse('hola' in self.st)

    def test7(self):
        self.st['hola'] = 'scope0'
        self.st.openScope()
        self.st['hola'] = 'scope1'
        self.st.openScope()
        self.st['hola'] = 'scope2'
        self.assertEqual(self.st['hola'], 'scope2')
        self.st.closeScope()
        self.assertEqual(self.st['hola'], 'scope1')
        self.st.closeScope()
        self.assertEqual(self.st['hola'], 'scope0')
