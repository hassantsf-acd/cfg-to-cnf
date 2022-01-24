class CFG:
    def __init__(self, start_variable='S', rules=None):
        if rules is None:
            rules = {}
        self.start_variable = start_variable
        self.unused_variables = set()
        self.init_variables()
        self.variables = set(self.unused_variables)
        self.rules = rules

    def init_variables(self):
        for i in range(65, 91):
            self.unused_variables.add(chr(i))
        self.unused_variables.add('S0')

    def add_rule(self, variable, rhs):
        if isinstance(rhs, set):
            self.rules[variable].update(rhs)
        else:
            if variable in self.rules:
                self.rules[variable].add(rhs)
            else:
                self.unused_variables.remove(variable)
                self.rules[variable] = {rhs}

    def remove_variable(self, variable, rhs):
        self.rules[variable].remove(rhs)

    def extend_rule(self, src, dest):
        self.rules[src] = self.rules[src].union(self.rules[dest])

    def get_unvisited_variable(self):
        return list(self.unused_variables)[len(self.unused_variables) - 1]

    def __str__(self):
        string = ""
        for variable, rhs in self.rules.items():
            string += f'{variable} -> {list(rhs)}\n'
        return string

    def __eq__(self, other):
        is_equal = True
        if other is None:
            return False
        if self.variables != other.variables:
            is_equal = False
        if self.rules != other.rules:
            is_equal = False
        if self.unused_variables != other.unused_variables:
            is_equal = False
        return is_equal
