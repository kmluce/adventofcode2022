import re


class Monkey:

    def __init__(self, monkey_number: int, starting_items: list, operation: str,
                 test: str, true_op: str, false_op: str):
        self.monkey_id = monkey_number
        self.items = starting_items
        self.operation_string = operation
        self.test_string = test
        self.true_string = true_op
        self.false_string = false_op

    def print_monkey_name(self):
        print(self.monkey_id, end=" ")

class GroupOfMonkeys:

    def __init__(self, first_monkey: Monkey):
        self.monkey_group = [first_monkey]

    def add_monkey(self, monkey: Monkey):
        self.monkey_group.append(monkey)

    def num_monkeys(self):
        self.print_list_of_monkeys()
        return len(self.monkey_group)

    def print_list_of_monkeys(self):
        for monkey in self.monkey_group:
            monkey.print_monkey_name()

class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.monkey_group: GroupOfMonkeys = None

    def parse(self):
        curr_monkey = -1
        curr_items = []
        curr_op = ''
        curr_test = ''
        curr_true = ''
        curr_false = ''
        with open(self.fileName) as file:
            for line in file:
                line = line.rstrip()
                print(line)
                if line.rstrip():
                    elements = re.search('Monkey *(\d+):', line)
                    if elements:
                        curr_monkey = elements.group(1)
                    else:
                        monkey_features = line.split(': ')
                        if re.search('Starting items', monkey_features[0]):
                            curr_items = monkey_features[1].split(', ')
                        elif re.search('Operation', monkey_features[0]):
                            curr_op = monkey_features[1]
                        elif re.search('Test', monkey_features[0]):
                            curr_test = monkey_features[1]
                        elif re.search('If true', monkey_features[0]):
                            curr_true = monkey_features[1]
                        elif re.search('If false', monkey_features[0]):
                            curr_false = monkey_features[1]
                else:
                    print("monkey:", curr_monkey)
                    print("  items:", curr_items)
                    print("     op:", curr_op)
                    print("   test:", curr_test)
                    print("   true:", curr_true)
                    print("  false:", curr_false)
                    if self.monkey_group:
                        self.monkey_group.add_monkey(Monkey(curr_monkey, curr_items, curr_op, curr_test,
                                                            curr_true, curr_false))
                    else:
                        self.monkey_group = GroupOfMonkeys(Monkey(curr_monkey, curr_items, curr_op,
                                                                  curr_test, curr_true, curr_false))
            if self.monkey_group:
                self.monkey_group.add_monkey(Monkey(curr_monkey, curr_items, curr_op, curr_test,
                                                    curr_true, curr_false))
            else:
                self.monkey_group = GroupOfMonkeys(Monkey(curr_monkey, curr_items, curr_op,
                                                  curr_test, curr_true, curr_false))

    def print(self):
        pass

    def solve(self):
        self.print()
        if self.puzzle_part == "a":
            return self.monkey_group.num_monkeys()
        else:
            return 0
