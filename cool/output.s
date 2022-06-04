
    .data
    .align  2
    .globl  class_nameTab
    .globl  Main_protObj
    .globl  Int_protObj
    .globl  String_protObj
    .globl  bool_const0
    .globl  bool_const1
    .globl  _int_tag
    .globl  _bool_tag
    .globl  _string_tag
_int_tag:
    .word   2
_bool_tag:
    .word   3
_string_tag:
    .word   4
    .word   -1
int_const0:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   1
    .word   -1
int_const2:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   4
    .word   -1
int_const1:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   5
    .word   -1
str_const0:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const0
    .ascii  """
    .byte   0
    .align  1
    .word   -1
str_const1:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const0
    .ascii  "t"
    .byte   0
    .align  1
    .word   -1
str_const2:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const0
    .ascii  "e"
    .byte   0
    .align  1
    .word   -1
str_const3:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const0
    .ascii  "s"
    .byte   0
    .align  1
class_nameTab:
    .word   str_const4
    .word   str_const5
    .word   str_const6
    .word   str_const7
    .word   str_const8
    .word   str_const9
class_objTab:
    .word   Object_protObj
    .word   Object_init
    .word   IO_protObj
    .word   IO_init
    .word   Int_protObj
    .word   Int_init
    .word   String_protObj
    .word   String_init
    .word   Bool_protObj
    .word   Bool_init
    .word   Main_protObj
    .word   Main_init
Object_dispTab:
    .word   Object.abort
    .word   Object.type_name
    .word   Object.copy
IO_dispTab:
    .word   IO.out_string
    .word   IO.out_int
    .word   IO.in_string
    .word   IO.in_int
    .word   Object.abort
    .word   Object.type_name
    .word   Object.copy
Int_dispTab:
    .word   Object.abort
    .word   Object.type_name
    .word   Object.copy
String_dispTab:
    .word   String.length
    .word   String.concat
    .word   String.substr
    .word   Object.abort
    .word   Object.type_name
    .word   Object.copy
Bool_dispTab:
    .word   Object.abort
    .word   Object.type_name
    .word   Object.copy
Main_dispTab:
    .word   Main.main
    .word   Object.abort
    .word   Object.type_name
    .word   Object.copy
    .word   -1
Object_protObj:
    .word   0
    .word   18
    .word   Object_dispTab
    .word   4
    .word   -1
IO_protObj:
    .word   1
    .word   3
    .word   IO_dispTab
    .word   -1
Int_protObj:
    .word   2
    .word   3
    .word   Int_dispTab
    .word   -1
String_protObj:
    .word   3
    .word   3
    .word   String_dispTab
    .word   -1
Bool_protObj:
    .word   4
    .word   3
    .word   Bool_dispTab
    .word   -1
Main_protObj:
    .word   5
    .word   3
    .word   Main_dispTab
    .word   -1
bool_const0:
    .word   3
    .word   4
    .word   Bool_dispTab
    .word   0
    .word   -1
bool_const1:
    .word   3
    .word   4
    .word   Bool_dispTab
    .word   1
   .globl  heap_start 
heap_start:
    .word   0 
    .text    
    .globl  Main_init 
    .globl  Int_init 
    .globl  String_init 
    .globl  Bool_init 
    .globl  Main.main 
