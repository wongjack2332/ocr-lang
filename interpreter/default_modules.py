"""
In this file we define default modules for the interpreter
"""
import random
from . import StringVal, RuntimeVal, MK_STRING
def get_default_modules() -> dict:
    modules = {
        "print": print,
        "random": random.randint,
        "input": input,
        "open": lambda x: FileHandler(x),
        "newFile": newFile,
    }

    return modules




def newFile(filename: StringVal = StringVal("")):
    with open(filename, "w") as f:
        pass
    file_handler = FileHandler(filename)
    return file_handler

class FileHandler(RuntimeVal):
    def __init__(self, filename: StringVal) -> None:

        self.filename = filename.value
        
        self.lines: list = []
        self.__get_lines()
        self.reading_lines = self.lines.copy()
        self.line_write = []
        self.method_set: dict = {
            "readLine": self.readLine,
            "writeLine": self.writeLine,
            "close": self.close,
            "readFile": self.readFile,
            "writeFile": self.writeFile
        }
        self.value = "File Handler for " + self.filename
    
    
    def __get_lines(self):
        file = self.filename
        with open(file, "r") as f:
            self.lines = f.read().strip().splitlines()
    def readLine(self) -> StringVal:
        if len(self.reading_lines) == 0:
            raise EOFError(f"End of file {self.filename}")
        return MK_STRING(self.reading_lines.pop(0))

    
    def writeLine(self, line) -> None:
        self.line_write.append(line)
    
    def writeFile(self, text) -> None:
        with open(self.filename, "w") as f:
            f.write(text)

    def readFile(self) -> StringVal:
        with open(self.filename, "r") as f:
            return MK_STRING(f.read())
    
    def close(self) -> None:
        self.writeFile(text="\n".join(self.line_write))
    
    # always put get_name method
    def get_name(self) -> str:
        return self.__class__.__name__
    