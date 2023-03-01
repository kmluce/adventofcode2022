import re
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
        self.debug.print(3, f"node {self.name} with flow {self.flow} and valve status {self.valve_on}")
        self.debug.print(3, f"     and tunnels are {self.tunnels}")
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
        self.debug.print(2, f"entered node {self.name}'s update route")
        self.print()
        self.debug.print(2, f"updating route to {old_dest} to go to {new_dest}")
        for x in self.tunnels:
            if x[1] == old_dest:
                tunnel_adds.append([x[0] + added_weight, new_dest, x[2] + new_dest])
                # x[1] = new_dest
                # x[0] = x[0] + added_weight
        self.tunnels.extend(tunnel_adds)
        self.debug.print(2, "route updated, here's new structure:")
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

    def add_node(self, name, flow, tunnels, debug=None):
        self.all_valves.append(TunnelNode(name, flow, tunnels, debug))

    def print(self):
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.all_valves)
        print("")
        self.debug.print(2, f"PRINTING entire tunnel map")
        self.debug.increase_indent
        for i in self.all_valves:
            i.print()
        self.debug.decrease_indent

    def find_node_from_name(self, node_name):
        matches = [x for x in self.all_valves if x.my_name() == node_name]
        if len(matches) > 1:
            print("ERROR: found more than one node for name", node_name)
            return None
        else:
            return matches[0]

    def update_route(self, node_name, orig_dest, new_dest, added_weight):
        self.debug.print(2, f"updating {node_name} from {orig_dest} to {new_dest} and adding weight {added_weight}")
        node_to_update = self.find_node_from_name(node_name)
        node_to_update.update_route(orig_dest, new_dest, added_weight)
        # node_to_update.remove_route(orig_dest)

    def remove_route(self, origin, destination):
        origin_node = self.find_node_from_name(origin)
        origin_node.remove_route(destination)

    def remove_node(self, node_to_remove):
        self.all_valves = [x for x in self.all_valves if x != node_to_remove]

    def update_node_paths(self, remove_node):
        # TODO: this probably does the wrong thing.  It needs to:
        #       * get all destinations from remove_node.
        #       * one by one, go to those node destinations and instantiate a path for EACH
        #         destination in remove_node except the self-referencing one.
        #       * remove the path directly to remove_node from each of those destination nodes
        #       * remove the remove_node
        self.debug.increase_indent()
        self.debug.print(2, f"UPDATING paths to remove node {remove_node.my_name()}:")
        remove_node.print()
        for node1_weight, node1_dest, node1_orig_dest in remove_node.my_tunnels():
            self.debug.print(2, f"tunnel to {node1_dest} originally to {node1_orig_dest} at weight {node1_weight}")
            self.debug.increase_indent()
            for node2_weight, node2_dest, node2_orig_dest in remove_node.my_tunnels():
                if node1_dest != node2_dest:
                    self.debug.print(2, f"need to update node {node1_dest} to go to {node2_dest} with orig dest {remove_node.my_name()} weight {node2_weight}")
                    self.update_route(node1_dest, remove_node.my_name(), node2_dest, node2_weight)
            self.debug.decrease_indent()
            self.debug.print(2, f"removing route to {remove_node.my_name()} from {node1_dest}")
            self.remove_route(node1_dest, remove_node.my_name())
        self.debug.decrease_indent()

    def optimize_graph(self):
        empty_nodes = []
        self.debug.print(3, f"Entered Optimize Graph function")
        self.debug.increase_indent()
        self.debug.print(2, f"number of valves is {len(self.all_valves)}")
        empty_nodes = [x for x in self.all_valves if x.my_flow() == 0 and x.my_name() != self.root_name]
        self.debug.print(2, f"number of empty_nodes (aside from root) is {len(empty_nodes)}")
        for i in empty_nodes:
            self.debug.print(2, f"routing around empty node {i.my_name()}")
            self.debug.increase_indent()
            self.update_node_paths(i)
            self.remove_node(i)
            self.debug.decrease_indent()
        print("")
        self.debug.print(2, f"OPTIMIZING the root node")
        self.update_node_paths(self.find_node_from_name(self.root_name))
        self.print()
        self.debug.decrease_indent()
        print("END")

    # def find_path(self):
    #     current_node = self.find_node_from_name(self.root_name)
    #     visited_nodes = set()
    #     flow_val = 0
    #     timer = 1
    #     while len(visited_nodes) <= len(self.all_valves) and timer < 30:
    #         pass


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
                z = re.match("Valve (\w+) has flow rate=(\d+); tunnel.*to valves? (.+)", line.rstrip())
                self.debug.print(4, f"found valve {z.group(1)} with flow {z.group(2)} and tunnels {z.group(3)}")
                self.tunnel_map.add_node(z.group(1), z.group(2), z.group(3).split(', '), self.debug)
            self.tunnel_map.print()
            # node.print()
        self.tunnel_map.optimize_graph()
        self.print()

    def solve(self):
        self.parse()
        self.print()
        if self.puzzle_part == "a":
            # return self.find_path()
            return 0
        else:
            return 0
