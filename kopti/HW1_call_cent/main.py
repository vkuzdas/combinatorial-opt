#!/usr/bin/env python3

import sys
import gurobipy as g

if __name__ == '__main__':
    inFile, outFile = sys.argv[1:]
    inFile = open(inFile, 'r')

    s = inFile.read().split(" ")
    d = [int(string) for string in s]  # converts string array to int array

    n = len(d)
    m = g.Model()

    x = m.addVars(n, vtype=g.GRB.INTEGER, name="x", lb=0)
    z = m.addVars(n, vtype=g.GRB.INTEGER, name="z", lb=0)

    for i in range(n):
        v = g.quicksum([x[j % 24] for j in range(i - 7, i+1)])
        m.addConstr(z[i] >= d[i] - v, "cons1")
        m.addConstr(z[i] >= v - d[i], "cons2")
        # m.addConstr(z[i] >= 0, "cons3")
        # m.addConstr(x[i] >= 0, "cons4")

    m.setObjective(
        g.quicksum([z[i] for i in range(n)]),
        g.GRB.MINIMIZE
    )
    m.optimize()

    print(int(m.ObjVal))
    f = open(outFile, 'w')
    f.write(str(int(m.ObjVal)))
    f.write("\n")
    for idx in range(n):
        f.write(str(int(x[idx].X)))
        f.write(" ")
    f.close()
