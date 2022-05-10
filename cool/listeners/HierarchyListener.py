from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.Klass import Klass, setBaseKlasses
from util.KlassRegistry import getKlassByString, klassRepeats
from util.Method import Method
from util.exceptions import inheritsselftype, inheritsbool, inheritsstring, badredefineint, redefinedobject, \
    selftyperedeclared, redefinedclass, dupformals, attrbadinit, attroverride


class HierarchyListener(coolListener):

    def __init__(self):
        # esto es para las clases basicas existan, declara la clase con atributos y metodos
        setBaseKlasses()
        self.currentClass: Klass = None

    # cualquier pruebas de la sigueinte requere los tipos de datos armados
    def enterKlass(self, ctx: coolParser.KlassContext):
        mainType = ctx.TYPE(0).getText()
        inheritance = None
        if ctx.TYPE(1):
            inheritance = ctx.TYPE(1).getText()

        self.__classCreationChecks(mainType, inheritance)

        if ctx.TYPE(1) is not None:
            clase = Klass(mainType, inheritance)
        else:
            clase = Klass(mainType)
        self.currentClass = clase

    def enterAtribute(self, ctx: coolParser.AtributeContext):
        self.__attrbadinitcheck(ctx)
        self.__attroverride(ctx)
        self.currentClass.addAttribute(ctx.ID().getText(), getKlassByString(ctx.TYPE().getText()))

    def exitMetodo(self, ctx: coolParser.MetodoContext):
        parsedparams = None
        if ctx.params:
            parsedparams = set()
            seen_param_names = set()
            for param in ctx.params:
                if type(param) == coolParser.Formal_ExpressionContext:
                    if param.ID().getText() in seen_param_names:
                        # Explanation: We keep track of the params that are parsed from text
                        # If any of them repeat, we simply raise the exception
                        raise dupformals()
                    parsed = frozenset([param.ID().getText(), param.TYPE().getText()])
                    seen_param_names.add(param.ID().getText())
                    parsedparams.add(parsed)

        m = Method(ctx.TYPE(), parsedparams)
        self.currentClass.addMethod(ctx.ID(), m)

    def enterInt(self, ctx: coolParser.IntContext):
        ctx.Tipo = getKlassByString("Int")

    def enterString(self, ctx: coolParser.StringContext):
        # hojas el atributo siempre se debe hacer para utilizarlo
        ctx.Tipo = getKlassByString("String")

    def enterBoolTrue(self, ctx: coolParser.BoolTrueContext):
        ctx.Tipo = getKlassByString("Bool")

    def enterBoolFalse(self, ctx: coolParser.BoolTrueContext):
        ctx.Tipo = getKlassByString("Bool")

    def exitBase(self, ctx: coolParser.BaseContext):
        # FIXME Temporary fix, since VariableContext is not defined.
        if not type(ctx.getChild(0)) is coolParser.VariableContext:
            ctx.Tipo = ctx.getChild(0).Tipo

    @staticmethod
    def __classCreationChecks(mainType, inheritance=None):
        if inheritance:
            if inheritance == 'SELF_TYPE':
                raise inheritsselftype()
            if inheritance == 'Bool':
                raise inheritsbool()
            if inheritance == 'String':
                raise inheritsstring()
        # si no hay herencia
        else:
            if mainType == 'Int':
                raise badredefineint()
            if mainType == 'Object':
                raise redefinedobject()
            if mainType == 'SELF_TYPE':
                raise selftyperedeclared()
        if klassRepeats(mainType):
            raise redefinedclass()

    def __attroverride(self, ctx):
        try:
            variablename = ctx.ID().getText()
            # First, check for the attribute existing on the class tree
            # A keyerror would mean the variable isn't defined
            # FIXME method params will not be checked.
            self.currentClass.lookupAttribute(variablename)
            # Secondly, if the attribute is on the class tree, but it's *not*
            # on the current class, it means we're redefining a parent attribute.
            if not self.currentClass.getOwnAttribute(variablename):
                # Explanation: See above
                raise attroverride()
        except KeyError:
            # Explanation: See above
            pass

    def __attrbadinitcheck(self, ctx):
        # If this is an add attribute with the shape [ID : TYPE  '<-' expr]
        # where expr is a variable, check if said variable exists on the class
        if ctx.expr():
            if type(ctx.expr()) == coolParser.BaseContext:
                if type(ctx.expr().children[0]) == coolParser.VariableContext:
                    try:
                        variablename = ctx.expr().children[0].getText()
                        # First, check for the attribute existing on the class tree
                        # A keyerror would mean the variable isn't defined
                        # FIXME method params will not be checked.
                        self.currentClass.lookupAttribute(variablename)
                    except KeyError:
                        # Explanation: See above
                        raise attrbadinit()
