import re
import copy
from utils.debugging import PrintDebug


class TunnelNode:
    def __init__(self, name, flow, tunnels, debug=None):
        self.name = name
        self.flow = int(flow)
        self.valve_on = False
        self.tunnels = [[1, x, x] for x in tunnels]
        self.debug = debug

    def print(self):
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self)
        self.debug.increase_indent()
        self.debug.print(2, f"node {self.name} with flow {self.flow} and valve status {self.valve_on}")
        self.debug.print(2, f"     and tunnels are {self.tunnels}")
        self.debug.decrease_indent()

    def my_name(self):
        return self.name

    def my_flow(self):
        return self.flow

    def my_tunnels(self):
        return self.tunnels

    def update_route(self, old_dest, new_dest, added_weight):
        tunnel_adds = []
        self.debug.increase_indent()
        self.debug.print(4, f"entered node {self.name}'s update route")
        self.print()
        self.debug.print(4, f"updating route to {old_dest} to go to {new_dest}")
        for x in self.tunnels:
            if x[1] == old_dest:
                tunnel_adds.append([x[0] + added_weight, new_dest, x[2] + new_dest])
                # x[1] = new_dest
                # x[0] = x[0] + added_weight
        self.tunnels.extend(tunnel_adds)
        self.debug.print(4, "route updated, here's new structure:")
        self.print()
        self.debug.decrease_indent()

    def remove_route(self, old_route):
        self.tunnels = [x for x in self.tunnels if x[1] != old_route]


class TunnelGraph:

    def __init__(self, root_name, debug=None):
        self.root_name = root_name
        self.root_obj = None
        self.all_valves = []
        self.debug = debug
        self.num_nodes = 0
        self.shortest_paths = []
        self.name_to_index = {}
        self.INFINITY = 1000000
        self.MAX_TIMER = 30
        self.node_set = set()

    def add_node(self, name, flow, tunnels, debug=None):
        self.all_valves.append(TunnelNode(name, flow, tunnels, debug))

    def print(self):
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.all_valves)
        print("")
        self.debug.print(2, f"PRINTING entire tunnel map, # nodes = {len(self.all_valves)}")
        self.debug.increase_indent()
        for i in self.all_valves:
            i.print()
        self.debug.decrease_indent()

    def find_node_from_name(self, node_name):
        matches = [x for x in self.all_valves if x.my_name() == node_name]
        if len(matches) > 1:
            print("ERROR: found more than one node for name", node_name)
            return None
        else:
            return matches[0]

    def update_route(self, node_name, orig_dest, new_dest, added_weight):
        self.debug.print(3, f"updating {node_name} from {orig_dest} to {new_dest} and adding weight {added_weight}")
        node_to_update = self.find_node_from_name(node_name)
        node_to_update.update_route(orig_dest, new_dest, added_weight)
        # node_to_update.remove_route(orig_dest)

    def remove_route(self, origin, destination):
        origin_node = self.find_node_from_name(origin)
        origin_node.remove_route(destination)

    def remove_node(self, node_to_remove):
        self.all_valves = [x for x in self.all_valves if x != node_to_remove]

    def update_node_paths(self, remove_node):
        self.debug.increase_indent()
        self.debug.print(3, f"UPDATING paths to remove node {remove_node.my_name()}:")
        remove_node.print()
        for node1_weight, node1_dest, node1_orig_dest in remove_node.my_tunnels():
            self.debug.print(3, f"tunnel to {node1_dest} originally to {node1_orig_dest} at weight {node1_weight}")
            self.debug.increase_indent()
            for node2_weight, node2_dest, node2_orig_dest in remove_node.my_tunnels():
                if node1_dest != node2_dest:
                    self.debug.print(3, f"need to update node {node1_dest} to go to {node2_dest} with orig dest"
                                        f"{remove_node.my_name()} weight {node2_weight}")
                    self.update_route(node1_dest, remove_node.my_name(), node2_dest, node2_weight)
            self.debug.decrease_indent()
            self.debug.print(3, f"removing route to {remove_node.my_name()} from {node1_dest}")
            self.remove_route(node1_dest, remove_node.my_name())
        self.debug.decrease_indent()

    def optimize_graph(self):
        self.debug.print(3, f"Entered Optimize Graph function")
        self.debug.increase_indent()
        self.debug.print(2, f"number of valves is {len(self.all_valves)}")
        empty_nodes = [x for x in self.all_valves if x.my_flow() == 0 and x.my_name() != self.root_name]
        self.debug.print(2, f"number of empty_nodes (aside from root) is {len(empty_nodes)}")
        for i in empty_nodes:
            self.debug.print(3, f"routing around empty node {i.my_name()}")
            self.debug.increase_indent()
            self.update_node_paths(i)
            self.remove_node(i)
            self.debug.decrease_indent()
        print("")
        self.debug.print(2, f"OPTIMIZING the root node")
        self.update_node_paths(self.find_node_from_name(self.root_name))
        self.print()
        self.debug.decrease_indent()
        self.debug.print(1, "Done with parsing")

    def print_path_matrix(self):
        self.debug.print(2, "")
        self.debug.print(2, f"PRINTING shortest path matrix")
        print_string = "  "
        for i in self.all_valves:
            print_string = print_string + f"{i.my_name():>8}"
        self.debug.print(2, print_string)
        for i in range(self.num_nodes):
            print_string = ""
            print_string = print_string + f"{self.all_valves[i].my_name():4}"
            for j in range(self.num_nodes):
                print_string = print_string + f"{self.shortest_paths[i][j]:>8}"
            self.debug.print(2, print_string)

    def find_all_shortest_paths(self):
        self.num_nodes = len(self.all_valves)
        self.shortest_paths = [[self.INFINITY for _j in range(self.num_nodes)] for _i in range(self.num_nodes)]
        for index in range(len(self.all_valves)):
            self.name_to_index[self.all_valves[index].my_name()] = index
        self.print_path_matrix()
        for node in self.all_valves:
            for weight, dest, orig_dest in node.my_tunnels():
                self.shortest_paths[self.name_to_index[node.my_name()]][self.name_to_index[dest]] = weight
        self.print_path_matrix()
        for k in range(len(self.all_valves)):
            for i in range(len(self.all_valves)):
                for j in range(len(self.all_valves)):
                    if self.shortest_paths[i][j] > self.shortest_paths[i][k] + self.shortest_paths[k][j]:
                        self.shortest_paths[i][j] = self.shortest_paths[i][k] + self.shortest_paths[k][j]
        self.node_set = set(self.all_valves)
        self.print_path_matrix()

    def find_path(self):
        current_node = self.find_node_from_name(self.root_name)
        visited_nodes = set()
        curr_path = []
        flow_val = 0
        timer = 0
        print("")
        result, new_path = self.find_best_path(current_node, timer, 1, flow_val, visited_nodes, curr_path)
        self.debug.print(2, f"found result with path:")
        self.print_path(new_path, 2)
        return result

    def print_path(self, path, debug_level):
        self.debug.increase_indent()
        for node, time in path:
            self.debug.print(debug_level, f"{time}: {node}")
        self.debug.decrease_indent()

    def find_best_path(self, curr_node, timer, depth, score, visited_nodes, curr_path):
        node_string = ""
        my_path = copy.copy(curr_path)
        best_path = curr_path
        curr_visited_nodes = copy.copy(visited_nodes)
        curr_visited_nodes.add(curr_node)
        my_path.append([curr_node.my_name(), timer])
        if timer > self.MAX_TIMER:
            return score, my_path
        tmp_unvisited = self.node_set.difference(curr_visited_nodes)
        self.debug.print(3, f"finding best path from {curr_node.my_name()} on"
                            f"minute {timer}, depth {depth}, and score {score}")
        self.debug.increase_indent()
        for next_node in curr_visited_nodes:
            node_string = node_string + " " + next_node.my_name()
        self.debug.print(4, f"nodes already visited are:  {node_string}")
        path_string = ""
        for node, time in best_path:
            path_string = path_string + " " + str(time) + ":" + node
        self.debug.print(4, f"best path so far is: {path_string}")
        best_val = score
        node_string = ""
        for next_node in tmp_unvisited:
            node_string = node_string + " " + next_node.my_name()
        self.debug.print(4, f"nodes remaining to check are:  {node_string}")
        for next_node in tmp_unvisited:
            self.debug.print(3, f"checking node {next_node.my_name()}")
            cost = self.shortest_paths[self.name_to_index[curr_node.my_name()]][self.name_to_index[next_node.my_name()]]
            valve_gain = next_node.flow * (self.MAX_TIMER - timer - cost - 1)
            self.debug.increase_indent()
            self.debug.print(4, f"cost to go from {curr_node.my_name()} to {next_node.my_name()} is {cost}")
            if (timer + cost) > self.MAX_TIMER - 1:
                self.debug.print(4, f"cost is too high, passing")
                self.debug.decrease_indent()
                pass
            else:
                self.debug.print(4, f"flow is {next_node.flow} so gain would be {valve_gain}")
                new_val, new_path = self.find_best_path(next_node, timer + cost + 1, depth + 1, score + valve_gain,
                                                        curr_visited_nodes, my_path)
                if new_val > best_val:
                    best_val = new_val
                    best_path = new_path
                self.debug.decrease_indent()
        self.debug.print(4, f"returning from recursion")
        self.debug.decrease_indent()
        return best_val, best_path


class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part, debug_level):
        self.fileName = file_name
        self.puzzle_part = puzzle_part
        self.debug = PrintDebug(debug_level)
        self.debug_level = debug_level
        self.tunnel_map = TunnelGraph("AA", self.debug)

    def print_run_info(self):
        self.debug.print(1, f"{chr(10)}PUZZLE RUN:  running part {self.puzzle_part} with file "
                            f"{self.fileName} and debug level {self.debug_level}")

    # def print(self, string_debug_level: int, debug_string: str):
    #     if string_debug_level <= self.debug_level:
    #         print(debug_string)

    def print(self):
        pass

    def parse(self):
        self.print_run_info()
        with open(self.fileName) as file:
            self.debug.increase_indent()
            for line in file:
                self.debug.print(4, f"matching on line {line.rstrip()}")
                z = re.match(r"Valve (\w+) has flow rate=(\d+); tunnel.*to valves? (.+)", line.rstrip())
                self.debug.print(4, f"found valve {z.group(1)} with flow {z.group(2)} and tunnels {z.group(3)}")
                self.tunnel_map.add_node(z.group(1), z.group(2), z.group(3).split(', '), self.debug)
            self.tunnel_map.print()
            # node.print()
        self.tunnel_map.optimize_graph()
        self.print()

    def solve(self):
        self.parse()
        self.tunnel_map.find_all_shortest_paths()
        self.print()
        if self.puzzle_part == "a":
            output_value = self.tunnel_map.find_path()
            print("output value is", output_value)
            return output_value
        else:
            return 0
