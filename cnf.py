from cfg import CFG
from string import ascii_lowercase, ascii_uppercase
from copy import deepcopy

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

set_of_elements_without_specified_char = set()

def create_subset_of_rules(string, element, no):
    global set_of_elements_without_specified_char
    try:
        string[no]
    except Exception:
        return
    if string[no] == element:
        without_element = string[:no] + string[no + 1:]
        with_element = string
        set_of_elements_without_specified_char.update([with_element, without_element])
        create_subset_of_rules(without_element, element, no)
        create_subset_of_rules(with_element, element, no + 1)
    else:
        create_subset_of_rules(string, element, no + 1)

def find_null_productions(cfg):
    null_producers = []
    for variable, rule in cfg.rules.items():
        if '' in rule:
            null_producers.append(variable)
            cfg.remove_variable(variable, '')
    return null_producers

def remove_null_productions(cfg):
    global set_of_elements_without_specified_char
    null_producers = find_null_productions(cfg)

    while null_producers:
        for variable, rule in cfg.rules.copy().items():
            adding_rules = set()
            for element in rule:
                for producer in null_producers:
                    if producer in element:
                        set_of_elements_without_specified_char = set()
                        create_subset_of_rules(element, producer, 0)
                        adding_rules.update(set_of_elements_without_specified_char)
            cfg.add_rule(variable, adding_rules)
        null_producers = find_null_productions(cfg)

def find_terminals_in_rule(cfg, rule):
    terminals = set()
    has_terminal, has_non_terminal = False, False
    for char in rule:
        if char in ascii_lowercase:
            has_terminal = True
            terminals.add(char)
        if char in cfg.rules.keys():
            has_non_terminal = True
    if has_terminal and has_non_terminal:
        return terminals


def remove_terminals_neighbourhood(cfg):
    cfg_terminals = set()
    for variable, rule in cfg.rules.copy().items():
        for element in rule:
            if terminals := find_terminals_in_rule(cfg, element):
                cfg_terminals |= terminals

    adding_rules = {}
    for terminal in cfg_terminals:
        new_variable = cfg.get_unvisited_variable()
        cfg.add_rule(new_variable, terminal)
        adding_rules[terminal] = new_variable


    for variable, rule in cfg.rules.copy().items():
        for element in rule:
            if terminals := find_terminals_in_rule(cfg, element):
                map_table = element.maketrans(adding_rules)
                replaced_rule = element.translate(map_table)
                cfg.remove_variable(variable, element)
                cfg.add_rule(variable, replaced_rule)

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
    # cfg.add_rule('S', 'ASB')
    # cfg.add_rule('A', 'aAS')
    # cfg.add_rule('A', 'a')
    # cfg.add_rule('A', 'B')
    # cfg.add_rule('A', '')
    # cfg.add_rule('B', 'SbS')
    # cfg.add_rule('B', 'A')
    # cfg.add_rule('B', 'bb')

    cfg.add_rule('S', 'ASA')
    cfg.add_rule('S', 'oB')
    cfg.add_rule('A', 'B')
    cfg.add_rule('A', 'S')
    cfg.add_rule('B', 'b')
    cfg.add_rule('B', '')

    last_cfg = None

    while last_cfg != cfg:
        last_cfg = deepcopy(cfg)
        eliminate_start_variable(cfg)
        remove_long_rhs(cfg)
        remove_unit_productions(cfg)
        remove_null_productions(cfg)
        remove_terminals_neighbourhood(cfg)

    print(cfg)

if __name__ == "__main__":
    main()
