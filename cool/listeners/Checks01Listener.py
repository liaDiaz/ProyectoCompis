from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.exceptions import *


class Checks01Listener(coolListener):

    def __init__(self):
        self.main = False

    def enterKlass(self, ctx: coolParser.KlassContext):
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True

    def exitProgram(self, ctx: coolParser.KlassContext):
        # Moved classchecks to HierarchyListener.py
        if not self.main:
            raise nomain()

    def enterAtribute(self, ctx: coolParser.AtributeContext):
        if ctx.ID().getText() == 'self':
            # raise manda la excepcion
            raise anattributenamedself()

    def enterLetDeclear(self, ctx: coolParser.LetDeclearContext):
        if ctx.ID().getText() == 'self':
            # raise manda la excepcion
            raise letself()

    def enterFormal_Expression(self, ctx):
        if ctx.ID().getText() == 'self':
            raise selfinformalparameter()
        if ctx.TYPE().getText() == 'SELF_TYPE':
            raise selftypeparameterposition()

    def enterAssign(self, ctx: coolParser.AssignContext):
        if ctx.ID().getText() == 'self':
            raise selfassignment()
