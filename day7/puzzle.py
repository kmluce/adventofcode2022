from anytree import Node, RenderTree, Resolver, PreOrderIter

__FSYS_SIZE__ = 70000000
__SPACE_NEEDED__ = 30000000

class Directory(Node):
    def __init__(self, name, parent=None, children=None):
        super(Node, self).__init__()
        self.name = name
        self.parent = parent
        self.files = []
        if children:
            self.children = children

    def add_file(self, name, size):
        self.files.append([name, int(size)])

    def get_files(self):
        return self.files

class Puzzle:
    fileName: str

    def __init__(self, file_name, puzzle_part):

        self.fileName = file_name
        self.puzzle_part = puzzle_part

    def parse(self):
        first_directory = True
        with open(self.fileName) as file:
            for line in file:
                line = line.rstrip()
                line_contents = line.split(" ")
                #print(line)
                if line_contents[0] == "$":
                    if line_contents[1] == "cd":
                        if first_directory:
                            first_directory = False
                            self.tree_root = Directory(line_contents[2])
                            self.curr_node = self.tree_root
                        elif line_contents[2] == '..':
                            self.curr_node  = self.curr_node.parent
                        else:
                            r = Resolver('name')
                            tmp_node = r.get(self.curr_node, line_contents[2])
                            self.curr_node = tmp_node
                elif line_contents[0] == 'dir':
                    #print("  creating directory", line_contents[1])
                    tmp_node = Directory(line_contents[1], parent=self.curr_node)
                    #self.print()
                else:
                    #print("  file is", line_contents[1], "size", line_contents[0])
                    self.curr_node.add_file(line_contents[1], line_contents[0])

    def print(self):
        print(RenderTree(self.tree_root))

    def solve(self):
        #self.print()
        target_size = 0
        if self.puzzle_part == "a":
            for node in PreOrderIter(self.tree_root):
                #print("working through size of", node.name)
                total_size = 0
                for file in node.get_files():
                    total_size += file[1]
                for child_node in node.descendants:
                    for file in child_node.get_files():
                        total_size += file[1]
                #print("total size of", node.name, "is", total_size)
                if total_size <= 100000:
                    target_size += total_size
            return target_size
        else:
            subtree_sizelist = []
            for node in PreOrderIter(self.tree_root):
                #print("working through size of", node.name)
                total_size = 0
                for file in node.get_files():
                    total_size += file[1]
                for child_node in node.descendants:
                    for file in child_node.get_files():
                        total_size += file[1]
                #print("total size of", node.name, "is", total_size)
                subtree_sizelist.append(total_size)
            subtree_sizelist.sort(reverse=True)
            #print("largest directory is", subtree_sizelist[0], "smallest is", subtree_sizelist[-1])
            #print("unused space is", __FSYS_SIZE__ - subtree_sizelist[0])

            prior_size = subtree_sizelist[0]
            for dirsize in subtree_sizelist[1:]:
                if __FSYS_SIZE__ - subtree_sizelist[0] + dirsize < __SPACE_NEEDED__:
                    break
                else:
                    prior_size = dirsize
            return prior_size


