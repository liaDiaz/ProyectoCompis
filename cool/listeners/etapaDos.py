from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.exceptions import *
from util.structure import getAllClasses


class etapaDos(coolListener):
    def __init__(self):
        pass

    def exitAdd(self, ctx: coolParser.AddContext):
        # validar es int
        if (ctx.expr(0).Tipo.name == 'Int') and (ctx.expr(1).Tipo.name == 'Int'):
            ctx.Tipo = ctx.expr(0).Tipo
        else:
            raise badarith()

    # Exit cuando te importa que ya haya sido visitado los hijos y enter no importa

    def extiEqual(self, ctx: coolParser.EqualContext):
        if (ctx.expr(0).Tipo.name == 'Int') and (ctx.expr(1).Tipo.name == 'Int'):
            ctx.Tipo = ctx.expr(0).Tipo
        else:
            raise badequalitytest()
        # if((ctx.expr(0).Tipo.name == 'Int' ) and ((ctx.expr(1).Tipo.name =='BoolTrue') or (ctx.expr(1).Tipo.name =='BoolFalse'))):
        #     raise badequalitytest2()

    def enterMetodo(self, ctx: coolParser.MetodoContext):
        if ctx.TYPE().getText() not in getAllClasses():
            # Explanation: Types are registered in the Class Tree. If the type isn't defined, it won't be in it.
            raise returntypenoexist()
        pass
        # TODO CHECK SELFTYPE actual type
        # if ctx.TYPE().getText() == "SELF_TYPE":
        # Explanation: We cannot return SELF_TYPE from a class that returns something else than SELF_TYPE
        # We throw this exception whenever our return type is SELF_TYPE
        # raise selftypebadreturn()
