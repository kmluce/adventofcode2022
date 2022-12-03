class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.shared_items = []
        self.priority = 0
        self.group = []
        self.set1 = {}
        self.set2 = {}
        self.set3 = {}

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                items = [ x for x in line.rstrip()]
                #print("data =", items)
                if self.puzzle_part == "a":
                    compart1 = [line[x] for x in range(0, int(len(items)/2))]
                    compart2 = [line[x] for x in range(int(len(items)/2), len(items))]
                    #print("    ", compart1)
                    #print("    ", compart2)
                    set1 = set(compart1)
                    set2 = set(compart2)
                    #self.shared_items.append([value for value in compart1 if value in compart2])
                    for i in (set1 & set2):
                        self.shared_items.append(i)
                        if ord(i) < 96:
                            self.priority += ord(i) - 38
                            #print("  adding", ord(i) -38, "for value", i)
                        else:
                            self.priority += ord(i) - 96
                            #print("  adding", ord(i) -96, "for value", i)
                else:
                    print("data =", items)
                    self.group.append(items)
                    if len(self.group) == 3:
                        print("  ", self.group)
                        self.set1 = set(self.group[0])
                        self.set2 = set(self.group[1])
                        self.set3 = set(self.group[2])
                        self.shared_items.append(next(iter(self.set1 & self.set2 & self.set3)))
                        self.group = []

    def sum_shared_items(self):
        for i in self.shared_items:
            if ord(i) < 96:
                self.priority += ord(i) - 38
                # print("  adding", ord(i) -38, "for value", i)
            else:
                self.priority += ord(i) - 96
                # print("  adding", ord(i) -96, "for value", i)

    def print(self):
        print("shared items are:", self.shared_items)

    def solve(self):
        self.print()
        if self.puzzle_part == 'a':
            return self.priority
        else:
            self.sum_shared_items()
            return self.priority

    def solveb(self):
        return 0
