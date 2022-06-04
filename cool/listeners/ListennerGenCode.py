from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from listeners.Writer import Writer
from util.internal.asm import *


class ListennerGenCode(coolListener):

    def __init__(self) -> None:
        self.writer = Writer()

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.writer.append("PITO")

    def exitProgram(self, ctx: coolParser.ProgramContext):
        self.writer.append("NEPE")
        self.writer.writeOut()
        
    def exitAdd(self, ctx: coolParser.AddContext):
        s = arithTpl()
        self.writer.append(s)
