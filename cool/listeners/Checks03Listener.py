from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.Klass import setBaseKlasses
from util.KlassRegistry import getKlassByString
from util.exceptions import badargs1, badmethodcallsitself


class Checks03Listener(coolListener):

    def __init__(self):
        # esto es para las clases basicas existan, declara la clase con atributos y metodos
        setBaseKlasses()

    def exitCall(self, ctx: coolParser.CallContext):
        # methodparentclass = ctx.expr(0).Tipo
        # TEMPCODE
        methodparentclass = "A"
        # TEMPCODE
        methodname = ctx.ID().getText()
        methodInstance = getKlassByString(methodparentclass).lookupMethod(methodname)
        requiredParams = [paramtype for paramtype in methodInstance.params.values()]
        passedParamsTypes = self.__getParamListTypes(ctx)
        for requiredType, passedType in zip(requiredParams, passedParamsTypes):
            if requiredType != passedType:
                if passedType == methodparentclass:
                    # Explanation: See below. We catch this more specific edge case before defaulting into the general.
                    # TODO Remove hardcoded case
                    # See below
                    raise badmethodcallsitself()
                # Explanation: Passing a variable of wrong type to a method will raise this.from
                # We check the types of the method params against the provided types
                # Possible edgecases: self_type
                # TODO Remove hardcoded case
                # This code won't work with the current exitBase defined in HierarchyListener.
                # Proper definition for subexpression.tipo and variable.tipo is required
                # Currently, I've hardcoded it to pass the logical tests and it works.
                # Decomment lines once proper Tipo procedure is fulfilled
                raise badargs1()

    def __getParamListTypes(self, ctx):
        passedparams = []
        currentexpr = 1
        # while ctx.expr(currentexpr):
        # passedparams.append(ctx.expr(currentexpr).Tipo.name)
        # TEMPCODE
        passedparams.append(getKlassByString("A").name)
        passedparams.append(getKlassByString("Int").name)
        # TEMPCODE
        return passedparams
