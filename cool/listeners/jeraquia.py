from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.exceptions import inheritsselftype, inheritsbool, inheritsstring, badredefineint, redefinedobject, \
    selftyperedeclared, redefinedclass
from util.structure import Klass, lookupClass, setBaseKlasses, klassRepeats


class jeraquiaListener(coolListener):

    def __init__(self):
        # esto es para las clases basicas existan, declara la clase con atributos y metodos
        setBaseKlasses()
        self.currentClass = None

    # cualquier pruebas de la sigueinte requere los tipos de datos armados
    def enterKlass(self, ctx: coolParser.KlassContext):
        clase = None
        #  si hay herencia
        if ctx.TYPE(1) is not None:
            if ctx.TYPE(1).getText() == 'SELF_TYPE':
                raise inheritsselftype()
            if ctx.TYPE(1).getText() == 'Bool':
                raise inheritsbool()
            if ctx.TYPE(1).getText() == 'String':
                raise inheritsstring()
        # si no hay herencia
        else:
            if ctx.TYPE(0).getText() == 'Int':
                raise badredefineint()
            if ctx.TYPE(0).getText() == 'Object':
                raise redefinedobject()
            if ctx.TYPE(0).getText() == 'SELF_TYPE':
                raise selftyperedeclared()

        if klassRepeats(ctx.TYPE(0).getText()) and ctx.TYPE(0).getText() != "Main":
            print("**" + ctx.TYPE(0).getText() + "**")
            raise redefinedclass()

        if ctx.TYPE(1) is not None:
            clase = Klass(ctx.TYPE(0).getText(), ctx.TYPE(1).getText())
        else:
            clase = Klass(ctx.TYPE(0).getText())
        # definiemos la clase en la que estoy
        self.currentClass = clase

    def enterAtribute(self, ctx: coolParser.AtributeContext):

        self.currentClass.addAttribute(ctx.ID().getText(), lookupClass(ctx.TYPE().getText()))

    # add metod metodo tipo de regreso y lista de parametros que recibe // addmethod

    def enterInt(self, ctx: coolParser.IntContext):
        ctx.Tipo = lookupClass("Int")

    def enterString(self, ctx: coolParser.StringContext):
        # hojas el atributo siempre se debe hacer para utilizarlo
        ctx.Tipo = lookupClass("String")

    def enterBoolTrue(self, ctx: coolParser.BoolTrueContext):
        ctx.Tipo = lookupClass("Bool")

    def enterBoolFalse(self, ctx: coolParser.BoolTrueContext):
        ctx.Tipo = lookupClass("Bool")

    def exitBase(self, ctx: coolParser.BaseContext):
        # FIXME Temporary fix, since VariableContext is not defined.
        if not type(ctx.getChild(0)) is coolParser.VariableContext:
            ctx.Tipo = ctx.getChild(0).Tipo

    # def exitVariable(self, ctx: coolParser.VariableContext):
    # ctx.Tipo = lookupClass("Variable")
