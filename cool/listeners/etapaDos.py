from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.exceptions import *


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
        pass
        # if ctx.TYPE().getText() == "SELF_TYPE":
            # Explanation: We cannot return SELF_TYPE
            # We throw this exception whenever our return type is SELF_TYPE
            # raise selftypebadreturn()
