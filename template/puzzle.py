class Puzzle:
    fileName: str

    def __init__(self, file_name):
        self.fileName = file_name

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                if line.rstrip():
                    line = line.rstrip()
                else:
                    pass

    def print(self):
        pass

    def solvea(self):
        self.print()
        return 0

    def solveb(self):
        return 0
