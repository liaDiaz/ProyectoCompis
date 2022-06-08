from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.Klass import setBaseKlasses
from util.KlassRegistry import getKlassByString
from util.exceptions import badargs1, badmethodcallsitself


class Checks03Listener(coolListener):

    def __init__(self):
        # esto es para las clases basicas existan, declara la clase con atributos y metodos
        setBaseKlasses()
        self.table = None
        self.currentKlass = None

    def enterKlass(self, ctx: coolParser.KlassContext):
        self.currentKlass = getKlassByString(ctx.TYPE(0).getText())

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.table = ctx.table

    def exitCall(self, ctx: coolParser.CallContext):
        methodparentclass = self.currentKlass.name
        methodname = ctx.ID().getText()
        try:
            # Method not in class
            methodInstance = getKlassByString(methodparentclass).lookupMethod(methodname)
        except KeyError:
            pass
        try:
            methodInstance = ctx.expr(0).Tipo.lookupMethod(methodname)
        except KeyError:
            # This is a weird state
            # Explanation: See below. We catch this more specific edge case before defaulting into the general.
            raise badmethodcallsitself()
        requiredParams = [paramtype for paramtype in methodInstance.params.values()]
        passedParamsTypes = self.__getParamListTypes(ctx)
        for requiredType, passedType in zip(requiredParams, passedParamsTypes):
            if requiredType != passedType:
                # Explanation: Passing a variable of wrong type to a method will raise this.from
                # We check the types of the method params against the provided types
                raise badargs1()

    def __getParamListTypes(self, ctx):
        passedparams = []
        currentexpr = 1
        while ctx.expr(currentexpr):
            passedparams.append(ctx.expr(currentexpr).Tipo.name)
            currentexpr += 1
        return passedparams 
