from collections import OrderedDict
from typing import MutableMapping


class SymbolTable(MutableMapping):
    """
    La diferencia entre una tabla de símbolos y un dict es que si la
    llave ya está en la tabla, entonces se debe lanzar excepción.
    """

    def __init__(self):
        self.dict = OrderedDict()

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        """Aquí, si key ya está, regresar excepción"""
        if key in self.dict:
            raise KeyError(key)
        self.dict[key] = value

    def __delitem__(self, key):
        del self.dict[key]

    def __iter__(self):
        return iter(self.dict)

    def __len__(self):
        return len(self.dict)

    def __repr__(self):
        return self.dict.__repr__()
