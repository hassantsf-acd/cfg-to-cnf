from cnf import *
from cfg import *
from tkinter import *
import re

def insert():
    text = cfg_text.get("1.0",'end-1c').split('\n')
    cfg_class = CFG()
    for line in text:
        line = re.split(r'->', line)
        variable = line[0].rstrip().lstrip()
        for rule in re.split(r'[\||\n]', line[1]):
            rule = rule.rstrip().lstrip()
            if rule == 'eps':
                rule = ''
            cfg_class.add_rule(variable, rule)
    cfg_output = apply_rules(cfg_class)
    cfg_ans_text.set(cfg_output)

# S -> ASA | aB
# A -> B | S
# B -> b | eps

root = Tk()
root.title("Convert CFG To CNF")

cfg_label = Label(root, text="Enter CNF as given format : ")
cfg_label.grid(row=0, column=0)

cfg_text = Text(root)
cfg_text.grid(row=1,column=0)

cfg_error_text = StringVar(root)
cfg_error = Label(root, textvariable=cfg_error_text)
cfg_error.grid(row=2, column=0)

submit_buttom = Button(root, text="Submit", fg="Black", command=insert)
submit_buttom.grid(row=3, column=0)

cfg_ans_text = StringVar(root)
cfg_ans = Label(root, textvariable=cfg_ans_text)
cfg_ans.grid(row=4, column=0)

root.mainloop()
