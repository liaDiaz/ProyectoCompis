from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import Klass, lookupClass, setBaseKlasses


class jeraquiaListener(coolListener):

    def __init__(self):
        # esto es para las clases basicas existan, declara la clase con atributos y metodos
        setBaseKlasses()
        self.currentClass = None

    # cualquier pruebas de la sigueinte requere los tipos de datos armados
    def enterKlass(self, ctx: coolParser.KlassContext):
        clase = None
        if ctx.TYPE(1) != None:
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
        ctx.Tipo = ctx.getChild(0).Tipo
