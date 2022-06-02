
class Writer:
    def __init__(self) -> None:
        self.output = ""

    def append(self,content :str):
        self.output += "\n" + content

    def writeOut(self):
        with open("output.s", "w") as file1:
            file1.write(self.output)