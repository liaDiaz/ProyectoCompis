from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from listeners.Writer import Writer
from util.DataSegmentDirector import DataSegmentDirector


class DataSegmentGenListener(coolListener):

    def __init__(self) -> None:
        self.writer = Writer()
        self.strings = []
        self.ints = []

    def exitProgram(self, ctx: coolParser.ProgramContext):
        self.writer.append(DataSegmentDirector.getDataSegment(self.strings, self.ints))
        self.writer.writeOut()

    def enterInt(self, ctx: coolParser.IntContext):
        self.ints += ctx.INTEGER().getText()

    def enterString(self, ctx: coolParser.StringContext):
        self.strings += ctx.STRING().getText()
