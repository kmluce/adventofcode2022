class Forest:
    def __init__(self):
        self.treemap = []
        self.lvisible = []   # trees visible from left
        self.scenic = []

    def add_line(self, line):
        self.treemap.append([int(x) for x in line])
        # self.print()

    def print(self):
        print("treemap:")
        for line in self.treemap:
            print("  ", line)
        print("lvisible:")
        for line in self.lvisible:
            print("  ", line)
        print("scenic:")
        for line in self.scenic:
            print("  ", line)

    def find_scenic(self):
        print("entering find_scenic")
        self.scenic = [[0 for number in group] for group in self.treemap]
        self.print()
        for treey in range(1, len(self.treemap) - 1):
            for treex in range(1, len(self.treemap[0]) - 1):
                dtrees = 0
                utrees = 0
                rtrees = 0
                ltrees = 0
                for curry in range(treey + 1, len(self.treemap)):
                    dtrees += 1
                    if self.treemap[curry][treex] >= self.treemap[treey][treex]:
                        break
                for curry in range(treey - 1, -1, -1):
                    utrees += 1
                    if self.treemap[curry][treex] >= self.treemap[treey][treex]:
                        break
                for currx in range(treex + 1, len(self.treemap[0])):
                    rtrees += 1
                    if self.treemap[treey][currx] >= self.treemap[treey][treex]:
                        break
                for currx in range(treex - 1, -1, -1):
                    ltrees += 1
                    if self.treemap[treey][currx] >= self.treemap[treey][treex]:
                        break
                self.scenic[treey][treex] = dtrees * utrees * ltrees * rtrees


    def process_maps(self):
        self.lvisible = [[0 for number in group] for group in self.treemap]
    #    self.scenic = self.lvisible
        self.print()
        # calculate leftwise
        for j in range(0, len(self.treemap)):
            highest_left = self.treemap[j][0]
            self.lvisible[j][0] = 1
            for i in range(1, len(self.treemap[j])):
                if self.treemap[j][i] > highest_left:
                    self.lvisible[j][i] = 1 | self.lvisible[j][i]
                    highest_left = self.treemap[j][i]
        # calculate rightwise:
        for j in range(0, len(self.treemap)):
            highest_right = self.treemap[j][-1]
            self.lvisible[j][-1] = 1
            for i in reversed(range(1, len(self.treemap[j]))):
                if self.treemap[j][i] > highest_right:
                    self.lvisible[j][i] = 1 | self.lvisible[j][i]
                    highest_right = self.treemap[j][i]
        # calculate from above:
        for i in range(0, len(self.treemap[0])):  # counting on the map being rectangular, here
            highest_above = self.treemap[0][i]
            self.lvisible[0][i] = 1
            for j in range(1, len(self.treemap)):
                if self.treemap[j][i] > highest_above:
                    self.lvisible[j][i] = 1 | self.lvisible[j][i]
                    highest_above = self.treemap[j][i]
        # calculate from below:
        for i in range(0, len(self.treemap[0])):  # counting on the map being rectangular, here
            highest_below = self.treemap[-1][i]
            self.lvisible[-1][i] = 1
            for j in reversed(range(1, len(self.treemap))):
                if self.treemap[j][i] > highest_below:
                    self.lvisible[j][i] = 1 | self.lvisible[j][i]
                    highest_below = self.treemap[j][i]
        self.print()

    def visible_trees(self):
        tree_total = 0
        for i in self.lvisible:
            tree_total = tree_total + sum(i)
        return tree_total

    def most_scenic(self):
        self.print()
        return max(max(x) for x in self.scenic)


class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.forest = Forest()
        self.fileName = file_name
        self.puzzle_part = puzzle_part

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                if line.rstrip():
                    self.forest.add_line(line.rstrip())
                else:
                    pass
            self.forest.process_maps()
            self.forest.find_scenic()

    def print(self):
        pass

    def solve(self):
        self.print()
        if self.puzzle_part == "a":
            return self.forest.visible_trees()
        else:
            return self.forest.most_scenic()
