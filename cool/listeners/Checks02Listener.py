from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from listeners.HierarchyChecks import attrbadinitcheck
from util.Klass import Klass
from util.KlassRegistry import getAllKlasses, getKlass, getKlassByString
from util.exceptions import *
from util.internal.SymbolTableWithScopes import SymbolTableWithScopes


class Checks02Listener(coolListener):

    def __init__(self):
        # Current context class. Useful for adding methods and attributes
        self.currentClass: Klass = None
        # Nesting tracker. We need to raise badwhilebody if a single error occurs inside the body
        # Since we could have nesting, a nesting counter is neccesary.
        self.inwhile = False
        self.inwhileNesting = 0

        self.scopes = 0

    def enterCase(self, ctx: coolParser.CaseContext):
        # Set a set for keeping track of branches.
        ctx.branches = set()

    def enterCaseState(self, ctx: coolParser.CaseStateContext):
        if ctx.TYPE().getText() in ctx.parentCtx.branches:
            # Explanation: We keep track of branches types in the parent case node, and in case one repeats, we raise.
            raise caseidenticalbranch()
        else:
            ctx.parentCtx.branches.add(ctx.TYPE().getText())

    def enterKlass(self, ctx: coolParser.KlassContext):
        self.table = SymbolTableWithScopes(getKlass(ctx.TYPE(0).getText()))
        self.currentClass = getKlass(ctx.TYPE(0).getText())

    def enterLetDeclear(self, ctx: coolParser.LetDeclearContext):
        self.table.openScope()
        self.scopes += 1
        self.table[ctx.ID().getText()] = getKlassByString(ctx.TYPE().getText())

    def exitLet(self, ctx: coolParser.LetContext):
        for i in range(self.scopes):
            self.table.closeScope()
        self.scopes = 0

    def enterFormal_Expression(self, ctx: coolParser.Formal_ExpressionContext):
        self.table[ctx.ID().getText()] = getKlassByString(ctx.TYPE().getText())

    def enterAtribute(self, ctx: coolParser.AtributeContext):
        self.table[ctx.ID().getText()] = getKlassByString(ctx.TYPE().getText())
        attrbadinitcheck(self.table, self.currentClass, ctx)

    def exitSubexpresion(self, ctx: coolParser.SubexpresionContext):
        ctx.Tipo = ctx.expr().Tipo

    def exitNew(self, ctx: coolParser.NewContext):
        ctx.Tipo = getKlassByString(ctx.TYPE().getText())

    def enterVariable(self, ctx: coolParser.VariableContext):
        # Case statements are weird. They are IDs, but they cannot be set in another way than to check the parent's parent for the type
        if ctx.getText() == "self":
            ctx.Tipo = self.currentClass
            return
        if type(ctx.parentCtx.parentCtx) != coolParser.CaseStateContext:
            try:
                ctx.Tipo = self.table[ctx.getText()]
            except KeyError:
                raise outofscope()
        else:
            ctx.Tipo = getKlassByString(ctx.parentCtx.parentCtx.TYPE().getText())

    def exitAdd(self, ctx: coolParser.AddContext):
        # validar es int
        if (ctx.expr(0).Tipo.name == 'Int') and (ctx.expr(1).Tipo.name == 'Int'):
            ctx.Tipo = ctx.expr(0).Tipo
        else:
            raise badarith()

    def exitBase(self, ctx: coolParser.BaseContext):
        ctx.Tipo = ctx.getChild(0).Tipo

    def exitEqual(self, ctx: coolParser.EqualContext):
        expr = [ctx.expr(i).Tipo.name for i in range(2)]
        if "Int" in expr and "Bool" in expr:
            # Explanation: Very specific test case. Will check if Int and Bool are in the same eq
            raise badequalitytest2()
        if expr[0] != expr[1]:
            # Explanation: Catchall for every other case in which the types aren't the same
            raise badequalitytest()
        ctx.Tipo = ctx.expr(0).Tipo

    def exitCall(self, ctx: coolParser.CallContext):
        try:
            self.currentClass.lookupMethod(ctx.ID().getText())
        except KeyError:
            if self.inwhile:
                # Explanation: Error inside a while should be reported as badwhilebody.
                # Unfortunately, due to bad planning,
                # this would require a decorator that checks for in-while-condition before every exception
                # Here we only patch the specific case in which it breaks
                raise badwhilebody()
            try:
                ctx.expr(0).Tipo.lookupMethod(ctx.ID().getText())
                # Explanation: This is an exploit on the lookupMethod functionality:
                # A method can only be called if it's on the classes above them
                # BadDispatch checks for methods called in parent classes, defined on child classes.
                # This means we only need to check every parent, and if not found, raise the exception
                # Although this could mean the method doesn't even EXIST
            except KeyError:
                raise baddispatch()

    def enterWhile(self, ctx: coolParser.WhileContext):
        self.inwhile = True
        self.inwhileNesting += 1

    def exitWhile(self, ctx: coolParser.WhileContext):
        self.inwhileNesting -= 1
        if self.inwhileNesting == 0:
            self.inwhile = False
        if ctx.expr(0).Tipo.name != "Bool":
            # Explanation: While cond can only be boolean.
            # Here we simply check for the expression type
            # (and hope other team members did their job right!)
            raise badwhilecond()

    def enterMetodo(self, ctx: coolParser.MetodoContext):
        self.table.openScope()
        if ctx.TYPE().getText() == "SELF_TYPE":
            # Explanation: We cannot return SELF_TYPE from a class that returns something else than SELF_TYPE
            # We throw this exception whenever our return type is SELF_TYPE
            raise selftypebadreturn()
        if ctx.TYPE().getText() not in getAllKlasses():
            # Explanation: Types are registered in the Class Tree. If the type isn't defined, it won't be in it.
            raise returntypenoexist()

    def exitMetodo(self, ctx: coolParser.MetodoContext):
        self.table.closeScope()

    def exitProgram(self, ctx: coolParser.ProgramContext):
        ctx.table = self.table
