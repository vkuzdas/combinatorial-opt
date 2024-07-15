#!/usr/bin/env python3
import gurobipy as g
import numpy as np
import sys


class MyStripe:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        if width == 1:
            self.rgb = np.empty((1, height))
        else:
            self.rgbL = np.empty((1, height))
            self.rgbR = np.empty((1, height))


class Pixel:
    # constructor
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return 'Pixel({},{},{})'.format(self.r, self.g, self.b)


def get_stripes():
    s = []
    for i in range(n):
        stripe = MyStripe(w, h)
        line = file.readline().split()
        numbers = [int(string) for string in line]
        if w == 1:
            # extract every 3rd element
            stripe.rgb = np.array(numbers)
        elif w > 1:
            triples = [numbers[i:i + 3] for i in range(0, len(line), 3)]
            gap = w - 1
            rgbLeft = []
            rgbRight = []
            for j in range(0, len(triples), w):
                for i in triples[j]:
                    rgbLeft.append(i)
                for i in triples[j + gap]:
                    rgbRight.append(i)
            stripe.rgbL = np.array(rgbLeft)
            stripe.rgbR = np.array(rgbRight)
        s.append(stripe)
    return s


def calc_dist(s1, s2):
    if s1.width == 1:
        a = np.absolute(s1.rgb - s2.rgb)
    else:
        a = np.absolute(s1.rgbL - s2.rgbR)
    return np.sum(a)


def get_distances():
    dst = [[0 for i in range(n + 1)] for j in range(n + 1)]
    for i in range(n + 1):
        for j in range(n + 1):
            if i == j:
                dst[i][j] = g.GRB.INFINITY  # diagonal, not dummy
                continue
            if i == n or j == n:
                dst[i][j] = 0  # dummy node distance
                continue
            if w == 1:  # matrix is symmetrical
                d = calc_dist(stripes[i], stripes[j])
                dst[i][j] = d
                dst[j][i] = d
                continue
            else:  # matrix is not symmetrical
                d1 = calc_dist(stripes[i], stripes[j])
                # this is flipped
                dst[j][i] = d1
                d2 = calc_dist(stripes[j], stripes[i])
                dst[i][j] = d2
                continue
    return dst


# https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/traveling_salesman/tsp_gcl.ipynb#scrollTo=zqu1OerGyR9-
def my_callback(model, where):
    if where == g.GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(x)

        # selected_edges = g.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
        selected = g.tuplelist()
        for i in range(nodes):
            for j in range(nodes):
                if vals[i, j] > 0.5:
                    selected.append((i, j))
        cycle = shortest_cycle(selected)

        edges = []
        for i in range(len(cycle)):
            # edges.append((cycle[i], cycle[(i + 1) % len(cycle)]))
            e1 = cycle[i]
            e2 = cycle[(i + 1) % len(cycle)]  # modulo shifts pointer to the beginning of the list
            edges.append((e1, e2))

        if len(cycle) < nodes:
            model.cbLazy(g.quicksum(x[i, j] for i, j in edges) <= len(cycle) - 1)


# https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/traveling_salesman/tsp_gcl.ipynb#scrollTo=zqu1OerGyR9-
def shortest_cycle(edges):
    unvisited = list(range(nodes))
    cycle = range(nodes)  # Dummy - guaranteed to be replaced
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

        if len(thiscycle) <= len(cycle):
            cycle = thiscycle  # New shortest subtour
    return cycle


if __name__ == '__main__':
    inFile, outFile = sys.argv[1:]
    file = open(inFile, 'r')

    # first line has three numbers: n, w, h
    n, w, h = map(int, file.readline().split())
    stripes = get_stripes()
    distances = get_distances()
    print(distances)

    # n+1 dummy node
    nodes = n + 1
    m = g.Model()
    m.Params.lazyConstraints = 1

    # x[i,j] = 1 if edge i->j is in the solution
    x = m.addVars(nodes, nodes, vtype=g.GRB.BINARY, name='x')

    # outgoing edge
    # m.addConstrs(g.quicksum(x[i, j] for i in range(nodes)) == 1 for j in range(nodes))
    # incoming edge
    # m.addConstrs(g.quicksum(x[j, i] for i in range(nodes)) == 1 for j in range(nodes))

    for i in range(nodes):
        # outgoing edge
        sum = g.quicksum(x[i, j] for j in range(nodes))
        m.addConstr(sum == 1, "Xij")

        # incoming edge
        sum = g.quicksum(x[j, i] for j in range(nodes))
        m.addConstr(sum == 1, "Xji")

        # no need for diagonal constraint since INF on diagonal
        # m.addConstr(x[i, i] == 0, "diagonal")

    m.setObjective(g.quicksum(distances[i][j] * x[i, j] for i in range(nodes) for j in range(nodes)), g.GRB.MINIMIZE)
    m.optimize(my_callback)


    res = []
    node = n # from dummy node
    for XX in range(n):
        for i in range(n):
            if x[node, i].x > 0.9:
                node = i #dest node becomes source node
                break
        res.append(node+1)

    print(res)
    f = open(outFile, 'w')
    for idx in res:
        f.write(str(idx)+" ")
    f.close()

