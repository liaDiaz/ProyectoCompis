import unittest

from util.Klass import setBaseKlasses
from util.KlassRegistry import getKlassByString


class KlassMethodsTests(unittest.TestCase):
    def setUp(self):
        setBaseKlasses()

    def tearDown(self) -> None:
        _allClasses = {}

    def test1(self):
        io = getKlassByString('IO')
        m = io.lookupMethod('out_int')
        self.assertTrue(m.type, 'Int')

    def test2(self):
        str = getKlassByString('String')
        m = str.lookupMethod('substr')
        self.assertTrue(m.params['l'], 'Int')
