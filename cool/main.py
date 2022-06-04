from antlr4 import *

from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser
from listeners.Checks01Listener import Checks01Listener
from listeners.Checks02Listener import Checks02Listener
from listeners.Checks03Listener import Checks03Listener
from listeners.DataSegmentGenListener import DataSegmentGenListener
from listeners.HierarchyListener import HierarchyListener
from util.KlassRegistry import clearKlassTree


def compile(file):
    clearKlassTree()
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    walker.walk(Checks01Listener(), tree)
    walker.walk(HierarchyListener(), tree)
    walker.walk(Checks02Listener(), tree)
    walker.walk(Checks03Listener(), tree)
    # walker.walk(TreePrinter(), tree)
    walker.walk(DataSegmentGenListener(), tree)


def dummy():
    raise SystemExit(1)


if __name__ == '__main__':
    compile('resources/semantic/input/badarith.cool')
