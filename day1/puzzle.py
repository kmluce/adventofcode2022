import heapq


class Puzzle:
    fileName: str

    def __init__(self, file_name):
        self.fileName = file_name
        self.elves = []

    def parse(self):
        self.elves.append(0)
        with open(self.fileName) as file:
            for line in file:
                if line.rstrip():
                    line = line.rstrip()
                    self.elves[-1] += int(line)
#                    print(line)
                else:
                    self.elves.append(0)

    def print(self):
        print(self.elves)

    def solvea(self):
        self.print()
        return max(self.elves)

    def solveb(self):
        return sum(heapq.nlargest(3, self.elves))
