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


def find_unit_productions(cfg):
    unit_productions = []
    for variable in cfg.rules:
        for rule in cfg.rules[variable]:
            if rule in cfg.variables:
                unit_productions.append((variable, rule))

    return unit_productions


def remove_unit_productions(cfg):
    unit_productions = find_unit_productions(cfg)

    while unit_productions:
        for unit in unit_productions:
            cfg.remove_variable(unit[0], unit[1])
            if unit[0] != unit[1]:
                cfg.extend_rule(unit[0], unit[1])
        unit_productions = find_unit_productions(cfg)


def remove_long_rhs(cfg):
    for rule in cfg.rules.copy():
        for rhs in cfg.rules[rule]:
            side = rhs
            while len(side) > 2:
                new_variable = cfg.get_unvisited_variable()
                cfg.add_rule(new_variable, side[:2])
                cfg.rules[rule].remove(side)
                side = new_variable + side[2:]
                cfg.rules[rule].add(side)


def main():
    # S -> ASB
    # A -> aAS|a|ε
    # B -> SbS|A|bb
    cfg = CFG()
    cfg.add_rule('S', 'ASB')
    cfg.add_rule('A', 'aAS')
    cfg.add_rule('A', 'a')
    cfg.add_rule('A', 'B')
    # cfg.add_rule('A', '')
    cfg.add_rule('B', 'SbS')
    cfg.add_rule('B', 'A')
    cfg.add_rule('B', 'bb')
    print(cfg.rules)

    eliminate_start_variable(cfg)
    print(cfg.rules)

    remove_long_rhs(cfg)
    print(cfg.rules)

    remove_unit_productions(cfg)
    print(cfg.rules)


if __name__ == "__main__":
    main()
