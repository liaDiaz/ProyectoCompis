from util.internal.SymbolTable import SymbolTable


class Method:
    """
    Se usa una tabla de símbolos lineal para
    almacenar los tipos de los parámetros.
    m1 = Method("Integer")
    m2 = Method("String", [("a", "Integer"), ("b", "Boolean")])
    """

    def __init__(self, returntype, params=None):
        self.type = returntype
        self.params = SymbolTable()
        if params:
            for x, y in params:
                self.params[x] = y
