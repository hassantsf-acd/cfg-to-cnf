from cfg import CFG

def start_in_rhs(cfg):
    for variable in cfg.rules:
        for rule in cfg.rules[variable]:
            if cfg.start_variable in rule:
                return True
    return False

def eliminate_start_variable(cfg):
    if not start_in_rhs(cfg):
        return
    
    cfg.start_variable = 'S0'
    cfg.add_rule('S0', 'S')    

# S -> ASB
# A -> aAS|a|ε
# B -> SbS|A|bb
cfg = CFG()
cfg.add_rule('S', 'ASB')
cfg.add_rule('A', 'aAS')
cfg.add_rule('A', 'a')
# cfg.add_rule('A', '')
cfg.add_rule('B', 'SbS')
cfg.add_rule('B', 'A')
cfg.add_rule('B', 'bb')
print(cfg.rules)

eliminate_start_variable(cfg)
print(cfg.rules)
