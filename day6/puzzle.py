class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.codes = []
        self.solutions = []

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                if line.rstrip():
                    self.codes.append(line.rstrip())

    def print(self):
        print(self.solutions)

    def solve(self):
        i = 0
        offset = 0
        if self.puzzle_part == "a":
            offset = 4
        else:
            offset = 14
        for line in self.codes:
            for i in range(0, len(line) - offset):
                unique_chars = set(list(line[i:i + offset]))
                #print("  chars:", line[i:i + offset], "set:", unique_chars, "length:", len(unique_chars))
                if not len(unique_chars) <  offset:
                    #print("  appending current index", i)
                    self.solutions.append(i + offset)
                    break
        self.print()
        return self.solutions[0]
