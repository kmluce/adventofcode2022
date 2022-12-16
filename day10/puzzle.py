import math
class cathode:

    def __init__(self):
        self.register_x = 1
        self.clock_cycle = 0
        self.next_check = 20
        self.check_increment = 40
        self.saved_signal_strengths = []
        self.picture = [[' ' for x in range(0, 41)] for y in range(0, 7)]

    def check_cycle(self, step):
        if self.clock_cycle + step >= self.next_check:
            self.saved_signal_strengths.append(self.next_check * self.register_x)
            self.next_check += self.check_increment
        pic_x = (self.clock_cycle) % 40
        pic_y = math.floor((self.clock_cycle) / 40)
        print("clock cycle is", self.clock_cycle, ", register is", self.register_x, "and coords are", pic_x, pic_y)
        if -1 <= (self.clock_cycle % 40) - self.register_x <= 1:
            self.picture[pic_y][pic_x] = '#'
        else:
            self.picture[pic_y][pic_x] = '.'


    def addx(self, value):
        step = 2
        self.check_cycle(0)
        self.clock_cycle += 1
        self.check_cycle(0)
        self.clock_cycle += 1
        self.check_cycle(0)
        self.register_x += value

    def noop(self):
        step = 1
        self.check_cycle(0)
        self.clock_cycle += step
        self.check_cycle(0)

    def signal_value(self):
        return sum(self.saved_signal_strengths)

    def print(self):
        print("")
        for i in range(0, len(self.picture)):
            string=""

            print(string.join(self.picture[i]))
            #print(self.picture[i])
class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.elf_cathode = cathode()

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                print(line.rstrip())
                elements = line.rstrip().split(" ")
                if elements[0] == 'noop':
                   # print("  noop")
                    self.elf_cathode.noop()
                elif elements[0] == 'addx':
                   # print("   addx")
                    self.elf_cathode.addx(int(elements[1]))
            self.print()


    def print(self):
        self.elf_cathode.print()

    def solve(self):
        self.print()
        if self.puzzle_part == "a":
            return self.elf_cathode.signal_value()
        else:
            return 0
