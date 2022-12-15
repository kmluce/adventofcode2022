class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.head = [0,0]
        self.tail = [0,0]
        self.tail_visited = set()
        self.tail_visited.add(tuple(self.tail))
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                direction, count = line.rstrip().split(' ')
                for _i in range(0,int(count)):
                    self.move_head(direction)

    def move_head(self, direction):
        match direction:
            case 'R':
                self.head[1] += 1
            case 'L':
                self.head[1] -= 1
            case 'D':
                self.head[0] += 1
            case 'U':
                self.head[0] -= 1
        #print("after head move:")
        #self.print()
        self.move_tail()
        #print("after tail move:")
        #self.print()

    def move_tail(self):
        x_diff = self.head[1] - self.tail[1]
        y_diff = self.head[0] - self.tail[0]
        if abs(x_diff) > 1 or abs(y_diff) > 1:
            if (abs(x_diff) + abs(y_diff)) > 2: # move diagonally
                if x_diff < 1:
                    self.tail[1] -= 1
                elif x_diff >= 1:
                    self.tail[1] += 1
                if y_diff < 1:
                    self.tail[0] -= 1
                elif y_diff >= 1:
                    self.tail[0] += 1
            else:
                if abs(x_diff) > abs(y_diff):
                    if x_diff < 1:
                        self.tail[1] -= 1
                    elif x_diff > 1:
                        self.tail[1] += 1
                else:
                    if y_diff < 1:
                        self.tail[0] -= 1
                    elif y_diff > 1:
                        self.tail[0] += 1
        self.tail_visited.add(tuple(self.tail))

    def print(self):
        x_coords = [x[1] for x in self.tail_visited]
        y_coords = [x[0] for x in self.tail_visited]
        min_x_coord = min(x_coords)
        min_y_coord = min(y_coords)
        adj_x = min(min_x_coord, self.head[1], self.tail[1])
        adj_y = min(min_y_coord, self.head[0], self.tail[0])
        print('y coordinates are:', y_coords)
        print('x coordinates are:', x_coords)
        print("  min, max y are:", min(y_coords), max(y_coords))
        print("  min, max x are:", min(x_coords), max(x_coords))
        print("     adjust values:", adj_y, ",", adj_x)
        print("Head:", self.head, "  Tail:", self.tail)
        map_size_y = max(max(y_coords) - min(y_coords) + 1, abs(self.head[0]), abs(self.tail[0]))
        map_size_x = max(max(x_coords) - min(x_coords) + 1, abs(self.head[1]), abs(self.tail[1]))
        print("    making rope map of size", map_size_y, map_size_x)
        ropemap = [['.' for x in range(0, map_size_x + 3)] for y in range(0, map_size_y + 3)]
        for i in range(0, len(x_coords)):
            ropemap[y_coords[i] - adj_y][x_coords[i] - adj_x] = "#"
        ropemap[self.head[0] - adj_y][self.head[1] - adj_x] = "H"
        print("      setting Head at", self.head[0] - adj_y, self.head[1] - adj_x)
        ropemap[self.tail[0] - adj_y][self.tail[1] - adj_x] = "T"
        print("      setting Tail at", self.tail[0] - adj_y, self.tail[1] - adj_x)
        for line in ropemap:
            print("    ", line)
        #print("want to put head at:", self.head[0] - adj_y, self.head[1] - adj_x)

    def solve(self):
        #self.print()
        if self.puzzle_part == "a":
            return len(self.tail_visited)
        else:
            return 0
