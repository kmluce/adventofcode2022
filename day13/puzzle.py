import ast

LEFT = -1
RIGHT = 1
EQUAL = 0


class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part, debug_level):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.left = []
        self.right = []
        self.in_order_indexes = []
        self.curr_index = 1
        self.left_assigned = False
        self.right_assigned = False
        self.packet_list = []
        self.sorted_packet_list = []
        self.debug_level = debug_level

    def print_run(self):
        if self.debug_level > 0:
            print("PUZZLE RUN:  running part", self.puzzle_part, "with file", self.fileName)
        else:
            pass

    def insertion_sort(self):
        if self.debug_level > 2:
            print("  initial copy list is", self.sorted_packet_list, "and length=", len(self.sorted_packet_list))
        for item in self.packet_list:
            if self.debug_level > 1: print("INSERTING item", item, "into list")
            if len(self.sorted_packet_list) == 0:
                self.sorted_packet_list.append(item)
                if self.debug_level > 2:
                    print("  appended item", item, "as first list item, list is now:")
                    for print_item in self.sorted_packet_list:
                        print("    ", print_item)
            else:
                for index in range(0, len(self.sorted_packet_list)):
                    if self.debug_level > 2:
                        print("  checking item", item, "against existing list item", self.sorted_packet_list[index])
                    if self.check_order(item, self.sorted_packet_list[index]) == LEFT:
                        if self.debug_level > 2:
                            print("    inserting", item, "into list, result is:")
                            for print_item in self.sorted_packet_list:
                                print("      ", print_item)
                        self.sorted_packet_list.insert(index, item)
                        break
                    elif index == len(self.sorted_packet_list) - 1:
                        self.sorted_packet_list.append(item)

    def parse(self):
        self.print_run()
        if self.puzzle_part == "a":
            with open(self.fileName) as file:
                for line in file:
                    if line.rstrip():
                        line = line.rstrip()
                        # print(line)
                        if not self.left_assigned:
                            self.left = ast.literal_eval(line.rstrip())
                            self.left_assigned = True
                            # print("left =", self.left)
                        elif not self.right_assigned:
                            self.right = ast.literal_eval(line.rstrip())
                            self.right_assigned = True
                            # print("right =", self.right)
                    else:
                        if self.debug_level > 1: print("")
                        if self.debug_level > 1: print("== Pair", self.curr_index)
                        order = self.check_order(self.left, self.right)
                        if self.debug_level > 1:
                            if order == LEFT:
                                print("  Inputs are in the right order")
                            elif order == RIGHT:
                                print("  Inputs are NOT in the right order")
                            else:
                                print("  ERROR: order is inconclusive")
                        self.left = []
                        self.right = []
                        self.left_assigned = False
                        self.right_assigned = False
                        if order == LEFT:
                            self.in_order_indexes.append(self.curr_index)
                        self.curr_index += 1
                if self.debug_level > 1: print("")
                if self.debug_level > 1: print("== Pair", self.curr_index)
                order = self.check_order(self.left, self.right)
                if self.debug_level > 1:
                    if order == LEFT:
                        print("  Inputs are in the right order")
                    elif order == RIGHT:
                        print("  Inputs are NOT in the right order")
                    else:
                        print("  ERROR: order is inconclusive")
                if order == LEFT:
                    self.in_order_indexes.append(self.curr_index)
        else:
            with open(self.fileName) as file:
                for line in file:
                    if line.rstrip():
                        self.packet_list.append(ast.literal_eval(line.rstrip()))
            self.packet_list.append(ast.literal_eval('[[2]]'))
            self.packet_list.append(ast.literal_eval('[[6]]'))
            self.insertion_sort()
            self.print()

    def print(self):
        if self.puzzle_part == "a":
            print("indexes that ran correctly:", self.in_order_indexes)
        else:
            print("Original:")
            for item in self.packet_list:
                print("  ", item)
            print("Sorted:")
            for item in self.sorted_packet_list:
                print("  ", item)

    def check_order(self, left, right):
        if self.debug_level >= 4: print("comparing", left, "to", right)
        if type(left) is str and type(right) is str:
            # print("  both are strings")
            pass
        elif type(left) is int and type(right) is int:
            # print("  both are ints")
            if left < right:
                # print("      returning 2 because left int smaller than right int")
                return LEFT
            elif left > right:
                # print("      returning 0 because right int smaller than left int")
                return RIGHT
            else:
                # print("      returning 1 because both ints are the same")
                return EQUAL
        elif type(left) is list and type(right) is list:
            # print("  both are lists, checking list from 0 to", len(left))
            if len(left) == 0 and len(right) > 0:
                # print("  returning 2 because index 0 does not exist in left list")
                return LEFT
            for index in range(0, len(left)):
                # print ("   comparing", index, "indexed value of", left, "and", right)
                if index >= len(right):
                    # print("      returning 0 because current index", index, "does not exist in right list")
                    return RIGHT
                else:
                    sub_order = self.check_order(left[index], right[index])
                    if sub_order == RIGHT:
                        return RIGHT
                    elif sub_order == LEFT:
                        return LEFT
                    elif index == len(left)-1 and index < len(right)-1:
                        # print("      returning 2 because index", index, "does not exist in left list")
                        return LEFT
        else:
            if type(left) is int:
                return self.check_order([left], right)
            else:
                return self.check_order(left, [right])

    def solve(self):
        self.print()
        if self.puzzle_part == "a":
            return sum(self.in_order_indexes)
        else:
            return (self.sorted_packet_list.index([[2]]) + 1) * (self.sorted_packet_list.index([[6]]) + 1)
