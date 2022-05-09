from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.dummy import dummyListener
from listeners.etapaDos import etapaDos
from listeners.jeraquia import jeraquiaListener

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    walker.walk(jeraquiaListener(), tree)
    walker.walk(etapaDos(), tree)
    walker.walk(dummyListener(), tree)

    

def dummy():
    raise SystemExit(1)

if __name__ == '__main__':
    compile('resources/semantic/input/badarith.cool')
