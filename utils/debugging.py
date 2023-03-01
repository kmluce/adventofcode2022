class PrintDebug:

    def __init__(self, debug_level, indent=0):
        self.debug_level = debug_level
        self.indent = indent

    def print(self, curr_debug_level, debug_string):
        if curr_debug_level <= self.debug_level:
            print(" " * self.indent * 2, end="")
            print(debug_string)

    def increase_indent(self):
        self.indent = self.indent + 1

    def decrease_indent(self):
        self.indent = self.indent - 1
