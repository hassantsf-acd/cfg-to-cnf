class CFG:
    def __init__(self, start_variable='S', rules={}):
        self.start_variable = start_variable
        self.unused_variables = []
        self.init_variables()
        self.rules = rules

    def init_variables(self):
        for i in range(65, 91):
            self.unused_variables.append(chr(i))

    def add_rule(self, variable, rhs):
        if variable in self.rules:
            self.rules[variable].append(rhs)
        else:
            self.unused_variables.remove(variable)
            self.rules[variable] = [rhs]


# S -> ASB
# A -> aAS|a|ε
# B -> SbS|A|bb
cfg = CFG()
cfg.add_rule('S', 'ASB')
cfg.add_rule('A', 'aAS')
cfg.add_rule('A', 'a')
cfg.add_rule('A', '')
cfg.add_rule('B', 'SbS')
cfg.add_rule('B', 'A')
cfg.add_rule('B', 'bb')
print(cfg.rules)
