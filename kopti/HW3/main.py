#!/usr/bin/env python3
import sys
from collections import deque

import numpy as np

def find_augmenting_path(g_orig, nbs, source, sink, parent):
    # keep track of the capacity of the path to each vertex in the graph
    capacity_to_vertex = [0 for _ in range(len(g_orig))]
    capacity_to_vertex[source] = np.inf

    queue = deque([source])
    while queue:
        node = queue.popleft()
        # For each neighbor of the current vertex
        for i in nbs[node]:
            # If there is available capacity and the neighbor has not been seen before in the search
            if g_orig[node][i].capa > g_orig[node][i].flow and parent[i] == -1:
                # Update the parent of the neighbor to the current vertex
                parent[i] = node
                # Update the capacity of the path to the neighbor vertex to be the minimum of the capacity of the path to
                # the current vertex and the available capacity on the edge between the current vertex and the neighbor
                capacity_to_vertex[i] = min(capacity_to_vertex[node], g_orig[node][i].capa - g_orig[node][i].flow)
                queue.append(i)
                if i == sink:
                    return capacity_to_vertex[sink]
    # If the search has not found an augmenting path to the sink, return 0
    return 0


def edmonds_karp(g_orig, nbs, source, sink):
    flow = 0
    # While there is an augmenting path from the source to the sink
    while True:
        # keep track of the parent of each vertex in the augmenting path
        parent = [-1] * len(g_orig)
        # Find the maximum capacity of the augmenting path using BFS and update the parent array
        max_capacity = find_augmenting_path(g_orig, nbs, source, sink, parent)
        # If there is no augmenting path, break
        if max_capacity == 0:
            break
        # Update the flow along the augmenting path
        flow = flow + max_capacity
        v = sink
        while v != source:
            u = parent[v]
            g_orig[u][v].flow += max_capacity
            g_orig[v][u].flow -= max_capacity
            v = u
    # Return the maximum flow in the graph
    return flow





class EDGE:
    def __init__(self, lb=0, flow=0, ub=0, capa=0):
        self.lb = lb
        self.flow = flow
        self.ub = ub
        self.capa = capa


def flow_is_feasible(g_orig):
    for i in range(len(g_orig[0])):
        if g_orig[0][i].flow != g_orig[0][i].capa:
            return False
    return True


if __name__ == "__main__":
    inFile, outFile = sys.argv[1:]
    file = open(inFile, 'r')

    # first line denotes number of customer and number of products
    c, p = map(int, file.readline().split())
    bounds = []
    products = []

    # c lines in format:   l u p1 p2 ... pn
    for i in range(c):
        ints = [int(x) for x in file.readline().split()]
        bounds.append((ints[0], ints[1]))
        products.append(ints[2:])

    # last line in format:   dp1 dp2 ... dpn
    demand = [int(x) for x in file.readline().split()]


    # create graph with 2 sources and 2 sinks
    g_orig = []
    g_orig.append([EDGE() for _ in range(c + p + 4)])  #source - LB
    g_orig.append([EDGE() for _ in range(c + p + 4)])  #source UB-LB
    for i in range(c):
        r = [EDGE() for _ in range(c + p + 4)]
        for k in products[i]:
            idx = c + k + 1
            r[idx] = EDGE(0, 0, 1, 1)
        g_orig.append(r)

    # product edge vedou do sink
    for i in range(p):
        r = [EDGE() for _ in range(c + p + 4)]
        lb = demand[i]
        r[-2] = EDGE(lb, 0, np.inf, np.inf)
        r[-1] = EDGE(lb, 0, np.inf, lb)
        g_orig.append(r)

    g_orig.append([EDGE() for _ in range(c + p + 4)])  # sink: np.inf
    g_orig.append([EDGE() for _ in range(c + p + 4)])  # sink_

    # fill SRC LB
    for id, val in enumerate(bounds):
        g_orig[0][id+2].capa = val[0]
        g_orig[1][id+2].capa = val[1] - val[0]

    g_orig[0][-2].capa = sum(demand)
    # sum all lower bounds
    g_orig[1][-1].capa = sum([x[0] for x in bounds])
    g_orig[-2][1].capa = np.inf

    s1 = 1
    s2 = 0
    t1 = len(g_orig)-2
    t2 = len(g_orig)-1


    # create list of neighbors for each vertex (for BFS)
    nbs = [[] for _ in range(len(g_orig))]
    for idx, row in enumerate(g_orig):
        for nbr, cell in enumerate(row):
            if cell.capa > 0:
                nbs[idx].append(nbr)
                nbs[nbr].append(idx)

    ########################
    ######  RUN ALGO  ######
    ########################

    # compute initial flow to check feasibility
    init_f = edmonds_karp(g_orig, nbs, s2, t2)


    # if initial flow is not feasible, write -1 to output file
    if not flow_is_feasible(g_orig):
        file = open(outFile, 'w+')
        file.write('-1\n')
        file.close()

    else:
        # compute final flow and write to output file
        final_f = edmonds_karp(g_orig, nbs, s1, t1)
        file = open(outFile, 'w+')

        # write final flow to output file
        for k in range(2, c + 2):
            for idx, edge in enumerate(g_orig[k]):
                if edge.flow == 1:
                    print(idx - (2 + c - 1), end=' ')
                    file.write(str(idx - (2 + c - 1)) + " ")
            print()
            file.write("\n")
        file.close()








