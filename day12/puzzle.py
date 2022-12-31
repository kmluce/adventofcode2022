class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.start_coords = []
        self.end_coords = []
        self.max_x = 0
        self.max_y = 0
        self.input_map = []
        self.elevation_map = []
        self.distance_map = []
        self.queue = []
        self.visited = []
        self.INFINITY = -2

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                if line.rstrip():
                    line = line.rstrip()
                    self.input_map.append([x for x in line])
                    curr_y = len(self.input_map)-1
                    # print("line is:", line)
                    # print("map line is:", self.input_map[curr_y])
                    if 'S' in self.input_map[curr_y]:
                        # print("    S in ", line)
                        self.start_coords = [curr_y, self.input_map[curr_y].index('S')]
                        self.input_map[self.start_coords[0]][self.start_coords[1]] = 'a'
                    if 'E' in self.input_map[curr_y]:
                        # print("    E in ", line)
                        self.end_coords = [curr_y, self.input_map[curr_y].index('E')]
                        self.input_map[self.end_coords[0]][self.end_coords[1]] = 'z'
                    self.elevation_map.append([ord(x)-96 for x in self.input_map[curr_y]])
                    self.distance_map.append([self.INFINITY for x in line])
                    self.visited.append([False for x in line])
                    self.max_y = curr_y
                    self.max_x = len(self.elevation_map[curr_y]) - 1
                else:
                    pass
            self.queue.append(self.start_coords)
            # print("   queue is currently:", self.queue)

    def print(self):
        # print("input map as text:")
        # for y in range(0, len(self.input_map)):
        #     for x in range(0, len(self.input_map[y])):
        #         print('{:2}'.format(self.input_map[y][x]), end =" ")
        #     print(" ")
        print("elevation map as numbers:")
        for y in range(0, len(self.elevation_map)):
            for x in range(0, len(self.elevation_map[y])):
                print('{:2}'.format(self.elevation_map[y][x]), end=" ")
            print(" ")
        print("distance map as numbers:")
        for y in range(0, len(self.distance_map)):
            for x in range(0, len(self.distance_map[y])):
                print('{:2}'.format(self.distance_map[y][x]), end=" ")
            print(" ")
        num_infinities = sum([lst.count(self.INFINITY) for lst in self.distance_map])
        print("number of infinite entries is", num_infinities)
        print("queue is:", self.queue)

    def distance(self, coords):
        return self.distance_map[coords[0]][coords[1]]

    def neighbors(self, coords):
        a = coords[0]
        b = coords[1]
        potential_neighbors = [[a-1, b], [a+1, b], [a, b-1], [a, b+1]]
        # [lst for lst in potential_neighbors if 3<=lst[0]<=6 and 0<=lst[1]<=5]
        neighbors = [lst for lst in potential_neighbors if 0 <= lst[0] <= self.max_y and 0 <= lst[1] <= self.max_x]
        return neighbors

    def unvisited_neighbors(self, coords):
        a = coords[0]
        b = coords[1]
        potential_neighbors = [[a-1, b], [a+1, b], [a, b-1], [a, b+1]]
        # [lst for lst in potential_neighbors if 3<=lst[0]<=6 and 0<=lst[1]<=5]
        neighbors = [lst for lst in potential_neighbors if 0 <= lst[0] <= self.max_y and 0 <= lst[1] <= self.max_x]
        # print("    checking if neighbors are visited:", coords, neighbors)
        neighbors = [lst for lst in neighbors if self.visited[lst[0]][lst[1]] is False]
        return neighbors

    def unvisited_pathed_neighbors(self, coords):
        a = coords[0]
        b = coords[1]
        potential_neighbors = [[a - 1, b], [a + 1, b], [a, b - 1], [a, b + 1]]
        # [lst for lst in potential_neighbors if 3<=lst[0]<=6 and 0<=lst[1]<=5]
        neighbors = [lst for lst in potential_neighbors if 0 <= lst[0] <= self.max_y and 0 <= lst[1] <= self.max_x
                     and self.visited[lst[0]][lst[1]] is False and self.distance_map[lst[0]][lst[1]] != self.INFINITY]
        return neighbors

    def reverse_dijkstra(self):
        self.distance_map[self.end_coords[0]][self.end_coords[1]] = 0
        # pure Dijkstra
        self.queue = [self.end_coords]
        # self.print()
        while self.queue:
            curr_coords = self.queue.pop(0)
            self.visited[curr_coords[0]][curr_coords[1]] = True
            for new_coords in self.unvisited_neighbors(curr_coords):
                # print(" neighbors of", curr_coords, "are", self.neighbors(curr_coords))
                if self.elevation_map[new_coords[0]][new_coords[1]] - \
                        self.elevation_map[curr_coords[0]][curr_coords[1]] >= -1:
                    if self.distance(curr_coords) + 1 <= self.distance(new_coords) \
                            or self.distance(new_coords) == self.INFINITY:
                        # print("setting elevation of", new_coords, "to distance", self.distance(curr_coords), "plus 1")
                        self.distance_map[new_coords[0]][new_coords[1]] = self.distance(curr_coords) + 1
            self.queue.extend([item for item in self.unvisited_pathed_neighbors(curr_coords) if item not in self.queue])
            self.queue.sort(key=self.distance)
            # self.print()
        self.print()
        solutions_space = [self.distance([a,b]) for a in range(0,self.max_y + 1) for b in range(0,self.max_x + 1) if
                           self.elevation_map[a][b] == 1 and self.distance([a, b]) != self.INFINITY]
        # print("solutions space is", solutions_space)
        return min(solutions_space)

    def solve(self):
        self.print()

        if self.puzzle_part == "a":
            self.distance_map[self.start_coords[0]][self.start_coords[1]] = 0
            # pure Dijkstra
            while self.queue:
                curr_coords = self.queue.pop(0)
                if curr_coords == self.end_coords:
                    break
                self.visited[curr_coords[0]][curr_coords[1]] = True
                for new_coords in self.unvisited_neighbors(curr_coords):
                    # print(" neighbors of", curr_coords, "are", self.neighbors(curr_coords))
                    if self.elevation_map[new_coords[0]][new_coords[1]] - \
                            self.elevation_map[curr_coords[0]][curr_coords[1]] <= 1:
                        if self.distance(curr_coords) + 1 <= self.distance(new_coords) \
                                or self.distance(new_coords) == self.INFINITY:
                            # print("setting elevation of", new_coords, "to distance",
                            # self.distance(curr_coords), "plus 1")
                            self.distance_map[new_coords[0]][new_coords[1]] = self.distance(curr_coords) + 1
                self.queue.extend([item for item in self.unvisited_pathed_neighbors(curr_coords)
                                   if item not in self.queue])
                self.queue.sort(key=self.distance)
                # self.print()
            return self.distance_map[self.end_coords[0]][self.end_coords[1]]
        else:
            return self.reverse_dijkstra()
