import ast


class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.left = []
        self.right = []
        self.in_order_indexes = []
        self.curr_index = 1

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                if line.rstrip():
                    line = line.rstrip()
                    print(line)
                    if not self.left:
                        self.left = ast.literal_eval(line.rstrip())
                        print("left =", self.left)
                    elif not self.right:
                        self.right = ast.literal_eval(line.rstrip())
                        print("right =", self.right)
                else:
                    print("CASE", self.curr_index)
                    order = self.check_order(self.left, self.right)
                    print("ORDER is", order)
                    print("")
                    self.left = []
                    self.right = []
                    if order == 2:
                        self.in_order_indexes.append(self.curr_index)
                    self.curr_index += 1

    def print(self):
        print("indexes that ran correctly:", self.in_order_indexes)

    def check_order(self, left, right):
        print("comparing", left, "to", right)
        # print(" type of left is", type(left), "and type of right is", type(right))
        # TODO:  this is wrong, the order of checking is very specifically specified. Check AFTER integer checks.
        if type(left) is str and type(right) is str:
            print("  both are strings")
        elif type(left) is int and type(right) is int:
            print("  both are ints")
            if left < right:
                print("      returning 2 because left int smaller than right int")
                return 2
            elif left > right:
                print("      returning 0 because right int smaller than left int")
                return 0
            else:
                print("      returning 1 because both ints are the same")
                return 1
        elif type(left) is list and type(right) is list:
            print("  both are lists, checking list from 0 to", len(left))
            for index in range(0, len(left)):
                print ("   comparing", index, "indexed value of", left, "and", right)
                if index >= len(right):
                    print("      returning 0 because current index", index, "does not exist in right list")
                    return 0
                else:
                    sub_order = self.check_order(left[index], right[index])
                    if sub_order == 0:
                        return 0
                    elif sub_order == 2:
                        return 2
                    elif index == len(left)-1 and index < len(right)-1:
                        print("      returning 2 because index", index, "does not exist in left list")
                        return 2

        else:
            if type(left) is int:
                return self.check_order([left], right)
            else:
                return self.check_order(left, [right])
        # if len(left) > len(right):
        #     print("  Right side ran out of items, so inputs are NOT in the right order")
        #     return False

    def solve(self):
        self.print()
        if self.puzzle_part == "a":
            return 0
        else:
            return 0
