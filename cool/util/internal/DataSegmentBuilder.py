from math import ceil

from util.internal.asm import *


def round_to_nearest(n, m):
    return (n + m - 1) // m * m


class DataSegmentBuilder:

    def __init__(self):
        # Init header to the bare minimum
        # Default base tags to 234
        self.inttag = 2
        self.booltag = 3
        self.stringTag = 4

        self.intCodeFragments = set()
        self.intIndexes = {}
        self.strCodeFragments = set()
        self.strIndexes = {}

        self.output = dataHeaderString + baseClassTagTemplate.substitute(intTag=self.inttag, boolTag=self.booltag,
                                                                         stringTag=self.stringTag)

    def addInt(self, number):
        """
        Adds an int to the final output
        :param number: The number the int object represents
        """
        if number in self.intIndexes:
            return
        intstr = intTemplate.substitute(idx=len(self.intIndexes), tag=self.inttag, value=number)
        self.intIndexes[number] = len(self.intCodeFragments)
        self.intCodeFragments.add(intstr)

    def addString(self, s: str):
        """
        Add a string to the data segment.
        :param s:
        :return:
        """
        if s in self.strIndexes:
            return

        # The template for the empty string is special
        if s == "":
            if 0 not in self.intIndexes:
                self.addInt(0)
            self.strCodeFragments.add(
                emptyStringTemplate.substitute(tag=self.stringTag, idx=len(self.strIndexes),
                                               sizeIdx=self.intIndexes[0]))
        else:
            size, strintindex, align = self.__getStringData(s)
            self.strCodeFragments.add(
                stringTemplate.substitute(tag=self.stringTag, idx=len(self.strIndexes), size=size, value=s, align=align,
                                          sizeIdx=strintindex))
        self.strIndexes[s] = len(self.strIndexes)

    def __appendInts(self):
        if not self.intCodeFragments:
            return
        for s in self.intCodeFragments:
            self.output += s

    def __appendStrings(self):
        if not self.strCodeFragments:
            return
        for s in self.strCodeFragments:
            self.output += s

    def __finishHeader(self):
        self.output += boolString + heapString + textString

    def __getStringData(self, s):
        """
        The easiest way to get stupid string alues
        """
        # First, get (or create) the int Object for representing the string's size
        # "Main" == 4
        if len(s) not in self.intIndexes:
            self.addInt(len(s))
        sizeidx = self.intIndexes[len(s)]
        # The size of the code fragment: 4 basic words + (len(s) + nullterminator)/wordsize
        size = ceil(4 + ((len(s) + 1) / 4))
        # The fragment is then padded with 0’s to a word boundary
        align = 0
        if not len(s) + 1 % 4 == 0:
            align = round_to_nearest(len(s) + 1, 4) - 1 - len(s) - 1
        return size, sizeidx, align

    def build(self):
        self.__appendInts()
        self.__appendStrings()
        self.__appendClassSegment()
        self.__finishHeader()
        return self.output

    def __appendClassSegment(self):
        self.__addNameTable()
        self.__addObjTable()
        self.__addDispatchTablesSegment()
        self.__generateProtoObjects()

    def __addNameTable(self):
        pass

    def __addDispatchTablesSegment(self):
        pass

    def __generateProtoObjects(self):
        pass

    def __addObjTable(self):
        pass
