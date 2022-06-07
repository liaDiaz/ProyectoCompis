#se quito final 
from tkinter import *
def caseACallExpr (self, node):
    self.label=self.label
    for pe in node.getExpr():
        pe.apply(self)
        self.out("sw","$a0","0($sp)",self.comment("call: Push parameter",[]))
        self.out("addiu","$sp","$sp","-4")
    self.out("move","$a0","$s0")
    self.out("bne","$a0","$zero",self.label,self.comment("call: protect from dispatch to void",[]))
    self.out("la","$a0","str_const0")
    self.out("li","$t1",node.getObjectId().getLine(),self.comment("call: line number",[]))
    self.out("jal","_dispatch_abort")
    self.out(self.label)
    self.out("lw","$t1","8($a0)",self.comment("call: ptr to dispatch table",[]))
    m=self.klass.getMethodTable().get(node.getObjectId().getText())
    self.out("lw","$t1",m.getAddress(),self.comment("call: method %s is offset %d",m.name,m.offset))
    self.out("jalr","$t1")

