from util.KlassRegistry import getKlassByString, setKlassByString, klassRepeats
from util.Method import Method
from util.exceptions import missingclass
from util.internal.HierarchyException import HierarchyException
from util.internal.SymbolTable import SymbolTable


class Klass:
    """
    Agrupación de features (atributos y métodos).
    """

    # Ojo, variable de clase no de instancia
    # para encontrar la clase de la que hereda

    def __init__(self, name, inherits="Object"):
        self.name = name
        self.inherits = inherits
        if self.name != "Object":
            self.validHierarchy()

        self.attributes = SymbolTable()
        self.methods = SymbolTable()
        setKlassByString(name, self)

    def validHierarchy(self):
        up = self.inherits
        # Buscar hacia arriba hasta llegar a object
        while up != "Object":
            # Si encuentro la clase que estoy definiendo -> ciclo
            if up == self.name:
                raise HierarchyException
            try:
                up = getKlassByString(up).inherits
            except KeyError:
                # Explanation: MissingClass happens whenever we inherit from a nonexistent class.
                # Going up the class hierarchy tree and not finding a key means the inherited class is nonexistent.
                raise missingclass()

    def addAttribute(self, attribute_name: str, attribute_type: str):
        try:
            # Busco el atributo, si no está (excepción), puedo agregarlo
            self.lookupAttribute(attribute_name)
            raise KeyError(attribute_name)
        except KeyError:
            self.attributes[attribute_name] = attribute_type

    def addMethod(self, name: str, method: Method):
        self.methods[name] = method

    def getOwnAttribute(self, name: str):
        """
        Lookup an attribute on this class only
        :param name:  A string, with the name of the param to search
        :return: The type of the param if it exists, None if it doesn't
        """
        if name in self.attributes:
            return self.attributes[name]
        return None

    def lookupAttribute(self, name: str):
        """
        Buscar un atributo en una clase, si no se encuentra, resolver
        por herencia (hasta Object donde da error si no está el attributo)
        """
        if name in self.attributes:
            return self.attributes[name]
        elif self.name == "Object":
            raise KeyError(name)
        else:
            return getKlassByString(self.inherits).lookupAttribute(name)

    def lookupMethod(self, name: str):
        if name in self.methods:
            return self.methods[name]
        elif self.name == "Object":
            raise KeyError(name)
        else:
            return getKlassByString(self.inherits).lookupMethod(name)

    def conforms(self, B):
        """
        self <= B, esto es, puedo asignar a una variable de esta clase
        un objeto de tipo B? De otro modo, es B de la misma clase que self o
        más particular?
        """
        if B.name == 'Object':
            return False
        if B.name == self.name:
            return True
        else:
            return self.conforms(getKlassByString(B.inherits))


def setBaseKlasses():
    """
    Mandar llamar a setBaseKlasses() para crear las declaraciones de las 5 clases básicas
    """

    # If we've already added the base classes, do not run again.
    if klassRepeats("Object"):
        return

    k = Klass('Object')
    k.addMethod('abort', Method('Object'))
    k.addMethod('type_name', Method('Object'))
    k.addMethod('copy', Method('SELF_TYPE'))

    k = Klass('IO')
    k.addMethod('out_string', Method('SELF_TYPE', [('x', 'String')]))
    k.addMethod('out_int', Method('SELF_TYPE', [('x', 'Int')]))
    k.addMethod('in_string', Method('String'))
    k.addMethod('in_int', Method('Int'))

    k = Klass('Int')

    k = Klass('String')
    k.addMethod('length', Method('Int'))
    k.addMethod('concat', Method('String', [('s', 'String')]))
    k.addMethod('substr', Method('String', [('i', 'Int'), ('l', 'Int')]))

    k = Klass('Bool')
