from typing import MutableMapping


class SymbolTableWithScopes(MutableMapping):
    """
    Esta versión de tabla de símbolos maneja scopes mediante una pila,
    guarda en el scope activo y busca en los superiores.
    """

    def __init__(self, klass):
        self.dict_list = [{}]
        self.last = 0
        self.klass = klass

    def __getitem__(self, key):
        for i in reversed(range(self.last + 1)):
            if key in self.dict_list[i].keys():
                return self.dict_list[i][key]
        return self.klass.lookupAttribute(key)

    def __setitem__(self, key, value):
        if key in self.dict_list[self.last]:
            raise KeyError(key)
        self.dict_list[self.last][key] = value

    def __delitem__(self, key):
        del self.dict_list[self.last][key]

    def __iter__(self):
        return iter(self.dict_list[self.last])

    def __len__(self):
        return len(self.dict_list[self.last])

    def closeScope(self):
        self.dict_list.pop()
        self.last = self.last - 1

    def openScope(self):
        self.dict_list.append({})
        self.last = self.last + 1

    def __repr__(self):
        return self.dict_list.__repr__()
