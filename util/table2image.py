#!/usr/bin/env python3

import subprocess
import sys
import os

def dotable(table, name):
    tex = """\\documentclass[preview]{{standalone}}
    \\usepackage{{array}}
    \\renewcommand{{\\rmdefault}}{{ptm}}
    \\newcolumntype{{C}}[1]{{>{{\\bfseries\\centering\\arraybackslash}}p{{#1}}}}
    \\newcolumntype{{B}}[1]{{>{{\\bfseries\\raggedright\\arraybackslash}}b{{#1}}}}
    \\usepackage[utf8]{{inputenc}}
    \\inputencoding{{utf8}}
    \\begin{{document}}
    {}
    \\end{{document}}"""

    width = max(map(lambda x: len(x), table))

    tabular = "\\begin{tabular}{|B{3cm}|C{5.5cm}|C{5.5cm}|}\n"

    for line in table:
        tabular += "\\hline\n"
        if len(line) == 1:
            tabular += "\\multicolumn{{{}}}{{|>{{\\bfseries}}l|}}{{{}}}\\\\\n".format(width, line[0])
        elif len(line) == width:
            tabular += " & ".join(line) + "\\\\\n"
        else:
            print(name + ": line has " + str(len(line)) + " cells, don't know how to handle")
            print(line)
            print("width: " + str(width))
            exit()

    tabular += "\\hline\n\\end{tabular}"
    tex = tex.format(tabular)
    print(tex)

    with open(name + ".tex", "w") as f:
        f.write(tex)

    subprocess.call(["pdflatex", name + ".tex"])
    subprocess.call(["convert", "-density", "300", name + ".pdf", "-quality", "90", name + ".png"])
    os.remove(name + ".tex")
    os.remove(name + ".aux")
    os.remove(name + ".log")
    os.remove(name + ".pdf")

tables = [[["test"], ["foo"], ["a", "b", "c"]], [["bar"], ["1", "2", "3"]]]

# TODO: remove
tables = []
for i in range(1, 15):
    table = []
    with open("../../hochzeit/table" + str(i) + ".csv", "r") as f:
        for l in f.readlines():
            table.append(list(map(lambda x: x.strip(), l.split(","))))
    tables.append(table)

for (i, table) in enumerate(tables):
    dotable(table, "table" + str(i+1))
