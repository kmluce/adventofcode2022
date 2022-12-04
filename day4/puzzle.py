class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.set1 = set()
        self.set2 = set()
        self.num_intersections = 0

    def parse(self):
        with open(self.fileName) as file:
            tmp_line = []
            for line in file:
                line = line.rstrip()
        #        print (line)
                tmp_line = line.split(",")
        #        print("  ", tmp_line)
                tmp_range = tmp_line[0].split("-")
        #        print("     ", tmp_range)
                self.set1 = set([*range(int(tmp_range[0]), int(tmp_range[1])+1,)])
        #        print("         ", self.set1)
                tmp_range = tmp_line[1].split("-")
        #        print("     ", tmp_range)
                self.set2 = set([*range(int(tmp_range[0]), int(tmp_range[1])+1,)])
        #        print("         ", self.set2)
                set_intersection = self.set1.intersection(self.set2)
                if self.puzzle_part == "a":
                    if not self.set1.difference(set_intersection):
                        self.num_intersections += 1
                    elif not self.set2.difference(set_intersection):
                        self.num_intersections += 1
                else:
                    if set_intersection:
                        self.num_intersections += 1

    def print(self):
        pass

    def solve(self):
        self.print()
        #if self.puzzle_part == "a":
        return self.num_intersections
