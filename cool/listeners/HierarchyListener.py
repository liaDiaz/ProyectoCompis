from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from listeners.HierarchyChecks import classCreationChecks, signaturechangecheck, parseParams, \
    differentparamtypeoverridecheck, attroverride, attrbadinitcheck
from util.Klass import Klass, setBaseKlasses
from util.KlassRegistry import getKlassByString
from util.Method import Method


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

        classCreationChecks(mainType, inheritance)

        if ctx.TYPE(1) is not None:
            clase = Klass(mainType, inheritance)
        else:
            clase = Klass(mainType)
        ctx.Tipo = clase
        self.currentClass = clase

    def enterAtribute(self, ctx: coolParser.AtributeContext):
        attrbadinitcheck(self.currentClass, ctx)
        attroverride(self.currentClass, ctx)
        attrtype = ctx.TYPE().getText()
        #curent klass agragake el atributo
    
        self.currentClass.addAttribute(ctx.ID().getText(), attrtype)
        #seteando el tipo
        ctx.Tipo = getKlassByString(attrtype)
        #setear tipo variable (ID)
        ctx.getChild(0).Tipo = getKlassByString(ctx.getChild(1).getText())

     

    def exitMetodo(self, ctx: coolParser.MetodoContext):
        parsedparams = parseParams(ctx)
        parsedMethod = Method(ctx.TYPE(), parsedparams)
        # Check for method override
        signaturechangecheck(self.currentClass, ctx, parsedMethod)
        differentparamtypeoverridecheck(self.currentClass, ctx, parsedMethod)
        self.currentClass.addMethod(ctx.ID().getText(), parsedMethod)

    def enterInt(self, ctx: coolParser.IntContext):
        ctx.Tipo = getKlassByString("Int")

    def enterString(self, ctx: coolParser.StringContext):
        ctx.Tipo = getKlassByString("String")

    def enterBoolTrue(self, ctx: coolParser.BoolTrueContext):
        ctx.Tipo = getKlassByString("Bool")

    def enterBoolFalse(self, ctx: coolParser.BoolTrueContext):
        ctx.Tipo = getKlassByString("Bool")

    def enterSubexpresion(self, ctx: coolParser.SubexpresionContext):
        ctx.Tipo = ctx.expr().Tipo

    def exitBase(self, ctx: coolParser.BaseContext):
        # # TODO FIXME Temporary fix, since VariableContext and SubexpresionContext is not defined.
        # if not type(ctx.getChild(0)) is coolParser.VariableContext and \
        #         not type(ctx.getChild(0)) is coolParser.SubexpresionContext:
            ctx.Tipo = ctx.getChild(0).Tipo
