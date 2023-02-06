import re


class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part, debug_level):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.debug_level = debug_level
        # Here starts the puzzle-specific variables
        self.coords_list = []
        self.max_input_coords = []
        self.min_input_coords = []
        self.x_size = 0
        self.y_size = 0
        self.shift_x = 0
        self.shift_y = 0
        self.sensor_reach_map = []
        self.distances_list = []
        self.beacons = []

    def print_run_info(self):
        self.print_debug(1, f"{chr(10)}PUZZLE RUN:  running part {self.puzzle_part} with file "
                            f"{self.fileName} and debug level {self.debug_level}")

    def print_debug(self, string_debug_level: int, debug_printable):
        if string_debug_level <= self.debug_level:
            print(debug_printable)

    def print(self):
        self.print_debug(1, f"{self.coords_list}")
        self.print_debug(1, f"distances: {self.distances_list}")
        if self.debug_level >= 3:
            lineno = 0
            for line in self.sensor_reach_map:
                print('{:>3}'.format(lineno), end=" ")
                for char1 in line:
                    print(char1, end=" ")
                print("")
                lineno += 1

    def parse(self):
        with open(self.fileName) as file:
            for line in file:
                self.print_debug(4, list(map(int, re.findall(r'-?\d+', line))))
                coords = list(map(int, re.findall(r'-?\d+', line)))
                self.coords_list.append([coords[0:2], coords[2:4]])
                self.distances_list.append(([coords[0:2], self.manhattan_dist(*self.coords_list[-1])]))
                self.beacons.append(coords[2:4])
            self.max_input_coords = [max([x[0] for y in self.coords_list for x in y]),
                                     max([x[1] for y in self.coords_list for x in y])]
            self.min_input_coords = [min([x[0] for y in self.coords_list for x in y]),
                                     min([x[1] for y in self.coords_list for x in y])]
            self.x_size = self.max_input_coords[0] - self.min_input_coords[0]
            self.y_size = self.max_input_coords[1] - self.min_input_coords[1]
            self.shift_x = self.min_input_coords[0]
            self.shift_y = self.min_input_coords[1]
            self.print_debug(2, f"min coords are {self.min_input_coords} and max are {self.max_input_coords}")

    def map_coords(self):
        self.print_debug(2, f"setting up coords with min {self.min_input_coords[0]},"
                         f"{self.min_input_coords[1]} and max {self.max_input_coords[0]}"
                         f", {self.max_input_coords[1]}")
        self.print_debug(2, f"map size is {self.x_size}, {self.y_size}")
        self.sensor_reach_map = [["." for _x in range(0, self.x_size + 1)] for _y in range(0, self.y_size + 1)]
        self.print_debug(4, f"actual map size is{len(self.sensor_reach_map)}, {len(self.sensor_reach_map[0])}")
        for sensor_coords in self.coords_list:
            self.sensor_reach_map[sensor_coords[0][1] - self.shift_y][sensor_coords[0][0] - self.shift_x] = 'S'
            self.sensor_reach_map[sensor_coords[1][1] - self.shift_y][sensor_coords[1][0] - self.shift_x] = 'B'

    def manhattan_dist(self, a, b):
        self.print_debug(4, f"a is {a}, b is {b}")
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Brute force was a terrible idea :-)
    def num_beacons(self, y):
        no_beacon = []
        for x in range(self.min_input_coords[0], self.max_input_coords[0] + 1):
            for [sensor, dist] in self.distances_list:
                if self.manhattan_dist(sensor, [x, y]) <= dist:
                    no_beacon.append([x, y])
                    break
        # print(no_beacon)
        print(len(no_beacon))
        return len([x for y in no_beacon if y not in self.beacons])

    def sensor_intersection(self, y):
        intersections = []
        consolidated_segments = []
        for [sensor, dist] in self.distances_list:
            self.print_debug(3, f"  checking sensor {sensor} and distance {dist} for intersection with {y}")
            if abs(sensor[1] - y) <= dist:
                self.print_debug(4, f"      sensor {sensor} intersects with y={y}")
                span = dist - abs(sensor[1] - y)
                # intersections.append([[max(self.min_input_coords[0], sensor[0] - span), y],
                #                       [min(self.max_input_coords[0], sensor[0] + span), y]])
                intersections.append([[sensor[0] - span, y],
                                      [sensor[0] + span, y]])
                self.print_debug(3, f"      added intersection {intersections[-1]}")
        self.print_debug(2, f"intersection segments: {intersections}")
        intersections.sort(key=lambda point: point[0][0])
        self.print_debug(2, f"intersections sorted: {intersections}")
        for [begin, end] in intersections:
            if not consolidated_segments:
                consolidated_segments.append([begin, end])
            elif begin[0] <= consolidated_segments[-1][1][0] + 1:
                if end[0] > consolidated_segments[-1][1][0]:
                    consolidated_segments[-1][1][0] = end[0]
            else:
                consolidated_segments.append([begin, end])
        self.print_debug(2, f"consolidated segments are: {consolidated_segments}")
        return consolidated_segments

    def solve_part_a(self, y):
        nonbeacon_points = 0
        consolidated_segments = self.sensor_intersection(y)
        for segment in consolidated_segments:
            nonbeacon_points += segment[1][0] - segment[0][0]
        return nonbeacon_points

    def solve_part_b(self, min_xy, max_xy):
        intersections = []
        for curr_y in range(0, max_xy + 1):
            points = 0
            self.print_debug(3, f"testing row {curr_y}")
            intersections = self.sensor_intersection(curr_y)
            if intersections[0][0][0] < 0:
                intersections[0][0][0] = 0
            if intersections[-1][1][0] > max_xy:
                intersections[-1][1][0] = max_xy
            self.print_debug(2, f"clipped intersections: {intersections}")
            for segment in intersections:
                points += segment[1][0] - segment[0][0] + 1
            self.print_debug(2, f"points in line y={curr_y} is {points}")
            if points <= max_xy:
                break
        return (intersections[0][1][0] + 1) * 4000000 + intersections[0][1][1]

    def solve(self):
        self.print_run_info()
        self.parse()
        # self.map_coords()
        self.print()
        if self.puzzle_part == "a" and self.fileName == "demo_data.txt":
            self.map_coords()
            self.print()
            # return self.num_beacons(10)
            return self.solve_part_a(10)
        elif self.puzzle_part == "a" and self.fileName == "test_data.txt":
            return self.solve_part_a(2000000)
            # return self.num_beacons(2000000)
        elif self.puzzle_part == "b" and self.fileName == "demo_data.txt":
            return self.solve_part_b(0,20)
        elif self.puzzle_part == "b" and self.fileName == "test_data.txt":
            return self.solve_part_b(0,4000000)
