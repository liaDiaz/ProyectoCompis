import textwrap
import unittest

from util.internal.DataSegmentBuilder import DataSegmentBuilder


class DataSegmentBuilderTests(unittest.TestCase):

    def setUp(self):
        self.builder = DataSegmentBuilder()

    def test_add_int(self):
        shouldbe = textwrap.dedent("""
            .word   -1
        int_const0:
            .word   2
            .word   4
            .word   Int_dispTab
            .word   0
        """)
        self.builder.addInt(0)
        self.assertMultiLineEqual(textwrap.dedent(self.builder.intCodeFragments.pop()), shouldbe)

    def test_add_empty_string(self):
        shouldbe = textwrap.dedent("""
            .word   -1
        str_const0:
            .word   4
            .word   5
            .word   String_dispTab
            .word   int_const0
            .byte   0
            .align  2
        """)
        self.builder.addString("")
        self.assertMultiLineEqual(textwrap.dedent(self.builder.strCodeFragments.pop()), shouldbe)

    def test_add_string(self):
        shouldbe = textwrap.dedent("""
            .word   -1
        str_const0:
            .word   4
            .word   6
            .word   String_dispTab
            .word   int_const0
            .ascii  "Main"
            .byte   0
            .align  2
        """)
        self.builder.addString("Main")
        self.assertMultiLineEqual(textwrap.dedent(self.builder.strCodeFragments.pop()), shouldbe)
        # self.assertIn("")
