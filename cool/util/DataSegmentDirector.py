from util.internal.DataSegmentBuilder import DataSegmentBuilder


class DataSegmentDirector:
    @staticmethod
    def getDataSegment(strings, ints):
        builder = DataSegmentBuilder()
        for s in strings:
            builder.addString(s)
        for i in ints:
            builder.addInt(i)

        return builder.build()
