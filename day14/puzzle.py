import re

ROCK = '#'
SAND = 'o'
SOURCE = '+'
EMPTY = '.'


class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part, debug_level):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.debug_level = debug_level
        self.rock_paths = []
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.source_x = 500
        self.source_y = 0
        self.sand_map = []
        self.x_size = 0
        self.y_size = 0
        self.shift_x = 0
        self.shift_y = 0
        self.grain_count = 0

    def print_run_info(self):
        self.print_debug(1, f"PUZZLE RUN:  running part {self.puzzle_part} with file "
                            f"{self.fileName} and debug level {self.debug_level}")

    def print_debug(self, string_debug_level: int, debug_string: str):
        if string_debug_level <= self.debug_level:
            print(debug_string)

    def print_data_structures(self):
        if self.debug_level > 0:
            print("Rock Paths:")
            for item in self.rock_paths:
                print("  ", item)
            print(f"Min, Max of X: {self.min_x}, {self.max_x}   Y:  {self.min_y}, {self.max_y}")
            print(f"Source: {self.source_x}, {self.source_y}")
            print("Map size:", self.x_size, ", ", self.y_size)
            for y in range(0, len(self.sand_map)):
                for x in range(0, len(self.sand_map[y])):
                    print(self.sand_map[y][x], end="")
                print("")
            print("")

    def initialize_sand_map(self):
        self.sand_map = [[EMPTY for x in range(0, self.x_size + 1)] for y in range(0, self.y_size + 1)]
        for coords_list in self.rock_paths:
            self.print_debug(3, f"Path: {coords_list!r}")
            [curr_x, curr_y] = coords_list.pop(0)
            curr_x = curr_x - self.shift_x
            curr_y = curr_y - self.shift_y
            self.print_debug(4, f"setting path at {curr_y}, {curr_x}  ({curr_y - self.shift_y}, {curr_x - self.shift_x})")
            self.sand_map[curr_y][curr_x] = ROCK
            for [new_x, new_y] in coords_list:
                new_x = new_x - self.shift_x
                new_y = new_y - self.shift_y
                if curr_x == new_x:
                    if curr_y < new_y:
                        for y in range(curr_y, new_y + 1):
                            self.print_debug(4, f"   writing rock at {y}, {curr_x}")
                            self.sand_map[y][curr_x] = ROCK
                    else:
                        for y in range(new_y, curr_y + 1):
                            self.print_debug(4, f"   writing rock at {y}, {curr_x}")
                            self.sand_map[y][curr_x] = ROCK
                elif curr_y == new_y:
                    if curr_x < new_x:
                        for x in range(curr_x, new_x + 1):
                            self.print_debug(4, f"   writing rock at {curr_y}, {x}")
                            self.sand_map[curr_y][x] = ROCK
                    else:
                        for x in range(new_x, curr_x + 1):
                            self.sand_map[curr_y][x] = ROCK
                curr_x = new_x
                curr_y = new_y
        if self.puzzle_part == 'b':
            self.sand_map.append([ROCK for x in range(0, self.x_size + 1)])
            self.sand_map.append([EMPTY for x in range(0, self.x_size + 1)])

    def parse(self):
        self.print_run_info()
        with open(self.fileName) as file:
            for line in file:
                if line.rstrip():
                    self.rock_paths.append([[int(y) for y in x.split(',')] for x in re.split('->', line.rstrip())])
                else:
                    pass
        # print([j[0] for i in self.rock_paths for j in i])
        self.min_x = min(min([j[0] for i in self.rock_paths for j in i]), 500)
        self.max_x = max(max([j[0] for i in self.rock_paths for j in i]), 500)
        self.min_y = min(min([j[1] for i in self.rock_paths for j in i]), 0)
        self.max_y = max([j[1] for i in self.rock_paths for j in i]) + 1
        self.x_size = self.max_x - self.min_x + 2
        self.y_size = self.max_y - self.min_y
        if self.puzzle_part == 'b':
            min_x_size = self.y_size * 2 + 3
            self.print_debug(3, f"checking for {self.x_size} < {min_x_size}")
            if self.x_size < min_x_size:
                self.x_size = min_x_size
        self.shift_x = self.min_x - 1
        self.shift_y = self.min_y
        if self.puzzle_part == 'b':
            self.shift_x = self.min_x - 1 - int(self.max_y / 2)
        self.print_data_structures()
        self.initialize_sand_map()
        self.print_data_structures()
        self.source_x = self.source_x - self.shift_x
        self.source_y = self.source_y - self.shift_y

    def drop_sand(self):
        infinite_sand = False
        grain_blocked = False
        while not infinite_sand:
            x = self.source_x
            y = self.source_y
            grain_blocked = False
            self.grain_count += 1
            while not grain_blocked:
                self.print_debug(3, f"testing {x}, {y}")
                if y + 1 >= len(self.sand_map):
                    grain_blocked = True
                    infinite_sand = True
                elif self.sand_map[y + 1][x] == EMPTY:
                    y = y + 1
                elif self.sand_map[y + 1][x] == ROCK or self.sand_map[y + 1][x] == SAND:
                    try:
                        if self.sand_map[y + 1][x - 1] == ROCK or self.sand_map[y + 1][x - 1] == SAND:
                            if self.sand_map[y + 1][x + 1] == ROCK or self.sand_map[y + 1][x + 1] == SAND:
                                self.sand_map[y][x] = SAND
                                grain_blocked = True
                                if y == self.source_y and x == self.source_x:
                                    infinite_sand = True
                            else:
                                y = y + 1
                                x = x + 1
                        else:
                            y = y + 1
                            x = x - 1
                    except IndexError as err:
                        print(f"ERROR while setting {x}, {y}:")
                        self.print_data_structures()
                        print(f"error was {err}")
                        return

    def print(self):
        pass

    def solve(self):
        self.print()
        if self.puzzle_part == "a":
            self.drop_sand()
            self.print_data_structures()
            return self.grain_count - 1
        else:
            self.print_data_structures()
            self.drop_sand()
            self.print_data_structures()
            return self.grain_count
