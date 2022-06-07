import random
from math import ceil

from util.KlassRegistry import getAllKlasses
from util.internal.asm import *


def round_to_nearest(n, m):
    return (n + m - 1) // m * m


def _buildObjectTableFragment():
    """
    Dead simple assembly. Refer to assembly.png
    :return:
    """
    objtableFrag = objectTableHeaderString

    for klass in getAllKlasses():
        objtableFrag += objectTableRowTemplate.substitute(name=klass)
    return objtableFrag


def _buildObjectDTFragment(klassInstance):
    """
    Iterate on klassInstance and get an asm fragment containing all of the methods in objects and parents
    :param klassInstance:
    :return:
    """
    fragment = dispatchTableHeaderTemplate.substitute(objectname=klassInstance.name)
    thing = klassInstance.getAllMethods()
    for obj, methods in thing.items():
        # cuz we have a KeysView instead of a method
        for method in list(methods):
            fragment += dispatchTableRowTemplate.substitute(objectname=obj, methodname=method)

    return fragment


def _buildDispatchTableFragment():
    """
    Create the dispatch table. All method names, included parents
    """
    output = ""
    for klassInstance in getAllKlasses().values():
        print(klassInstance.name)
        output += _buildObjectDTFragment(klassInstance)
    return output


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
                                                                         stringTag=self.stringTag) + memoryManagerString

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
        self.__addProtoObjects()

    def __addNameTable(self):
        self.output += self._buildNameTableFragment()

    def _buildNameTableFragment(self):
        """
        Build a simple name table, with all the base objects in order and the rest in the hierarchical order.
        """
        baseKlasses = ['Object', 'IO', 'Int', 'Bool', 'String']
        nameTableFragment = nameTabHeaderString
        # Add base klass strings in case they don't exist.
        # Strict order needed
        for klass in baseKlasses:
            self.addString(klass)
            # Generate the first rows for base klasses
            nameTableFragment += nameTabRowTemplate.substitute(idx=self.strIndexes[klass])
        # Generate rows for new klasses
        for klass in getAllKlasses().keys():
            if klass in baseKlasses:
                continue
            self.addString(klass)
            nameTableFragment += nameTabRowTemplate.substitute(idx=self.strIndexes[klass])
        return nameTableFragment

    def __addDispatchTablesSegment(self):
        self.output += _buildDispatchTableFragment()

    def __addProtoObjects(self):
        self.output += self._buildProtoObjects()

    def __addObjTable(self):
        self.output += _buildObjectTableFragment()

    def _buildProtoObjects(self):
        output = ""
        counter = 0
        for klass in getAllKlasses().values():
            output += protoObjectTableHeaderTemplate.substitute(objectname=klass.name)
            # Build variable rows
            attributeRows = []

            if klass.getAllAttributes():
                # f1xme how do these work?
                for attr in klass.getAllAttributes().keys():
                    attributeRows += wordTemplate.substitute(content=random.randint(0, 10))

            # Add size of object
            output += protoObjectTableTemplate.substitute(classCounter=counter, numberofRows=len(attributeRows) + 3,
                                                          objname=klass.name)
            for a in attributeRows:
                output += a

            counter += 1

        return output
