class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.container_description = []
        self.instructions = []
        self.container_map = []

    def parse(self):
        with open(self.fileName) as file:
            map_phase = True
            for line in file:
                if line.rstrip():
                    line = line.rstrip()
                    if map_phase:
                        print("line:", line)
                        print("  ", line[1::4])
                        if '[' in line:
                            self.container_description.append(line[1::4])
                            self.insert_map_line(line[1::4])
                    else:
                        print("line:", line)
                        print("  ", line.split(" "))
                        self.instructions.append(line.split(" "))
                        self.execute_move(line.split(" "))
                else:
                    map_phase = False

    def insert_map_line(self, map_line):
        for i in range(0, len(map_line)):
            if len(self.container_map) < i+1:
                print("size of container map", len(self.container_map), "is less than current stack", i)
                self.container_map.append([])
            if not map_line[i] == ' ':
                self.container_map[i].insert(0, map_line[i])

    def execute_move(self, instruction_line):
        num_crates = int(instruction_line[1])
        from_index = int(instruction_line[3]) -1
        to_index = int(instruction_line[5]) -1
        tmp_crates = []
        print("got line", instruction_line, "so moving", num_crates, "from", from_index, "to", to_index)
        if self.puzzle_part == "a":
            for _ in range(num_crates):
                self.container_map[to_index].append(self.container_map[from_index].pop())
        else:
            for _ in range(num_crates):
                tmp_crates.insert(0, self.container_map[from_index].pop())
            print("tmp_crates is", tmp_crates)
            self.container_map[to_index].extend(tmp_crates)

    def print(self):
        print("container description is", self.container_description)
        print("container map is", self.container_map)
        print("instructions are", self.instructions)

    def solve(self):
        result=''
        self.print()
        for i in range(0, len(self.container_map)):
            result = result + self.container_map[i][-1]
        return result
