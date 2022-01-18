class CFG:
    def __init__(self, start_variable='S', rules={}):
        self.start_variable = start_variable
        self.unused_variables = []
        self.init_variables()
        self.variables = list(self.unused_variables)
        self.rules = rules

    def init_variables(self):
        for i in range(65, 91):
            self.unused_variables.append(chr(i))
        self.unused_variables.append('S0')

    def add_rule(self, variable, rhs):
        if variable in self.rules:
            self.rules[variable].append(rhs)
        else:
            self.unused_variables.remove(variable)
            self.rules[variable] = [rhs]

    def remove_variable(self, variable, rhs):
        self.rules[variable].remove(rhs)

    def extend_rule(self, src, dest):
        self.rules[src] += self.rules[dest]