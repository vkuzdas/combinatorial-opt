#!/usr/bin/env python3

import sys
import gurobipy as g
import numpy as np
"""
The goal of the kidney exchange problem is to
find a set of mutually disjoint cycles C′ ⊆ C(G) which maximizes the sum of preferences of the
performed compatible transplantations, i.e.,
"""



# https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/traveling_salesman/tsp_gcl.ipynb#scrollTo=zqu1OerGyR9-
def my_callback(model, where):
    if where == g.GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(x)
        # selected_edges = g.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
        selected = g.tuplelist()
        for i in range(n):
            for j in range(n):
                if vals[i, j] > 0.5:
                    selected.append((i, j))
        cycle = longest_cycle(selected)

        edges = []
        for i in range(len(cycle)):
            # edges.append((cycle[i], cycle[(i + 1) % len(cycle)]))
            e1 = cycle[i]
            e2 = cycle[(i + 1) % len(cycle)]  # modulo shifts pointer to the beginning of the list
            edges.append((e1, e2))
        if len(cycle) > L:
            # lazy contraint zajistuje, ze cyklus bude mit maximalne L uzlu
            model.cbLazy(g.quicksum(x[i, j] for i, j in edges) <= len(cycle) - 1)


# https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/traveling_salesman/tsp_gcl.ipynb#scrollTo=zqu1OerGyR9-
def longest_cycle(edges):
    unvisited = list(range(n))
    cycle = []  # Dummy - guaranteed to be replaced
    while unvisited:  # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)

            # neighbors = [j for i, j in edges.select(current, '*') if j in unvisited]
            neighbors = []
            for i, j in edges.select(current, '*'):
                if j in unvisited:
                    neighbors.append(j)

        if len(thiscycle) >= len(cycle):
            cycle = thiscycle  # New shortest subtour
    return cycle



if __name__ == '__main__':
    inFile, outFile = sys.argv[1:]
    file = open(inFile, 'r')

    n, m, L = map(int, file.readline().split())
    dist = np.matrix(np.ones((n,n)) * -g.GRB.INFINITY)
    for i in range(m):
        src_node, dst_node, P = map(float, file.readline().split())
        dist[int(src_node), int(dst_node)] = P


    # PRINT INPUT ---------------------------------------------------------------
    # for i in range(len(dist)):
    #     print(dist[i])
    # [print(row) for row in dist]


    # MODEL ---------------------------------------------------------------------
    m = g.Model()
    m.Params.lazyConstraints = 1
    x = m.addVars(n,n, vtype=g.GRB.BINARY, name='x')
    # 'vazebni' prommena y zarucuje, ze uzel v cyklu bud bude a nebo nikoliv
    # zadani totiz specifikuje, ze nektere uzly nemusi byt v zadnem cyklu
    y = m.addVars(n, vtype=g.GRB.BINARY, name='y')


    # CONSTRAINTS ---------------------------------------------------------------
    for i in range(n):
        # outgoing edge
        sum = g.quicksum(x[i, j] for j in range(n))
        m.addConstr(sum == y[i], "Xij")
        # incoming edge
        sum = g.quicksum(x[j, i] for j in range(n))
        m.addConstr(sum == y[i], "Xji")

    m.setObjective(g.quicksum(x[i,j] * dist[i,j] for i in range(n) for j in range(n)), g.GRB.MAXIMIZE)

    m.optimize(my_callback)


    # PRINT SOLUTION ------------------------------------------------------------
    f = open(outFile, 'w')
    f.write(str(round(m.objVal, 2)) + '\n' if round(m.objVal, 2) > 0.5 else '0.0\n')
    [f.write(str(i) + ' ' + str(j) + '\n') for i in range(n) for j in range(n) if x[i, j].X > 0.5];
    f.close()
