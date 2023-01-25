class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part, debug_level):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.debug_level = debug_level

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                if line.rstrip():
                    line = line.rstrip()
                else:
                    pass

    def print(self):
        pass

    def solve(self):
        self.print()
        if self.puzzle_part == "a":
            return 0
        else:
            return 0
