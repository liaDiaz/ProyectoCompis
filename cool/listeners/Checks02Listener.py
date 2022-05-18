from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.Klass import Klass
from util.KlassRegistry import getAllKlasses, getKlass
from util.exceptions import *


class Checks02Listener(coolListener):
    def __init__(self):
        # Current context class. Useful for adding methods and attributes
        self.currentClass: Klass = None
        # Nesting tracker. We need to raise badwhilebody if a single error occurs inside the body
        # Since we could have nesting, a nesting counter is neccesary.
        self.inwhile = False
        self.inwhileNesting = 0

    def enterKlass(self, ctx: coolParser.KlassContext):
        self.currentClass = getKlass(ctx.TYPE(0).getText())

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

    def enterCall(self, ctx: coolParser.CallContext):
        try:
            self.currentClass.lookupMethod(ctx.ID().getText())
        except KeyError:
            if self.inwhile:
                # Explanation: Error inside a while should be reported as badwhilebody.
                # Unfortunately, due to bad planning,
                # this would require a decorator that checks for in-while-condition before every exception
                # Here we only patch the specific case in which it breaks
                raise badwhilebody()
            # Explanation: This is an exploit on the lookupMethod functionality:
            # A method can only be called if it's on the classes above them
            # BadDispatch checks for methods called in parent classes, defined on child classes.
            # This means we only need to check every parent, and if not found, raise the exception
            # Although this could mean the method doesn't even EXIST
            raise baddispatch()

    def enterWhile(self, ctx: coolParser.WhileContext):
        self.inwhile = True
        self.inwhileNesting += 1

    def exitWhile(self, ctx: coolParser.WhileContext):
        self.inwhileNesting -= 1
        if self.inwhileNesting == 0:
            self.inwhile = False
        if ctx.expr(0).Tipo.name not in ["Bool", "Int"]:
            # Explanation: While cond can only be boolean or int.
            # Here we simply check for the expression type
            # (and hope other team members did their job right!)
            raise badwhilecond()

    def enterMetodo(self, ctx: coolParser.MetodoContext):
        if ctx.TYPE().getText() == "SELF_TYPE":
            # Explanation: We cannot return SELF_TYPE from a class that returns something else than SELF_TYPE
            # We throw this exception whenever our return type is SELF_TYPE
            raise selftypebadreturn()
        if ctx.TYPE().getText() not in getAllKlasses():
            # Explanation: Types are registered in the Class Tree. If the type isn't defined, it won't be in it.
            raise returntypenoexist()
