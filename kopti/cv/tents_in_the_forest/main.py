import gurobipy as g

import matplotlib.pyplot as plt
import numpy
import numpy as np


def visualize(n, trees, tents, r, c):
    grid = [["." for _ in range(n + 2)] for _ in range(n + 2)]

    for t_x, t_y in tents:
        grid[t_y][t_x] = "X"

    for t_x, t_y in trees:
        grid[t_y][t_x] = "T"

    print("  ", end="")
    for c_cur in c:
        print(c_cur, end=" ")
    print()

    for y in range(1, n + 1):
        print(r[y - 1], end=" ")
        for x in range(1, n + 1):
            print(grid[y][x], end=" ")

        print()

n = 3
r = (1, 1, 0)
c = (1, 0, 1)
trees = [(1,1), (3,2)]

# Model ---------------------------------------
m = g.Model()

is_tree = [
    [False for i in range(n+2)] # radek falsu o n+2 bunkach
    for i in range(n+2) # n+2-krat radek falsu
]

for x, y in trees:
    is_tree[x][y] = True


# MODEL ---------------------------------------

m = g.Model()
dirs = ['u', 'r', 'd', 'l']
a = m.addVars(n+2, n+2, dirs, vtype=g.GRB.BINARY) # a(x,y,'u') na pozici x,y je stan prichyceny nahoru
M = 8

for x in range(1, n+1):
    for y in range(1, n+1):
        if not is_tree[x][y]:
            m.addConstr(a.sum(x-1,y,'l') + a.sum(x+1,y,'r') + a.sum(x,y-1,'d') + a.sum(x,y+1,'u') == 0,name="no attached tent")
        elif is_tree[x][y]:
            m.addConstr(a.sum(x,y,'*') == 0,name="tent neni tam kde strom")
            m.addConstr(a.sum(x-1,y,'l') + a.sum(x+1,y,'r') + a.sum(x,y-1,'d') + a.sum(x,y+1,'u') == 1,name="has attached tent")

        m.addConstr(M*(1-a.sum(x,y,'*')) >=
                    a.sum(x-1,y-1,'*') + a.sum(x-1,y,'*') + a.sum(x-1,y+1,'*') +
                    a.sum(x,y-1,'*') +                      a.sum(x,y-1,'*') +
                    a.sum(x+1,y-1,'*') + a.sum(x+1,y,'*') + a.sum(x+1,y+1,'*')
                    )
        m.addConstr(a.sum(x,y,'*') <= 1,name="pouze jeden tent na policku")


# pocet stanu ve sloupci a radku
for i in range(1,n+1):
    m.addConstr(a.sum('*',i,'*') == r[i-1], name="prescribed count row")  # suma v i tem radku
    m.addConstr(a.sum(i,'*','*') == c[i-1], name="prescribed count col")

# dummy edges
m.addConstr(a.sum(0,'*','*') == 0, name="first row empty")
m.addConstr(a.sum(n+1,'*','*') == 0, name="last row empty")
m.addConstr(a.sum('*', 0,'*') == 0, name="first col empty")
m.addConstr(a.sum('*', n+1,'*') == 0, name="last col empty")

m.optimize()

print(" ", end=' ')
print(c)
# Visualize -----------------------------------
g = [['.' for _ in range(n+2)] for _ in range(n+2)]
for x in range(1, n+1):
    for y in range(1, n+1):

        # kdyz je stan, vytikni kterym smerem
        if a.sum(x, y, '*').getValue() > 0.5:
            for z in dirs:
                if a[x,y,z].x > 0.5:
                    g[y][x] = z
                    print("tent on position", x, y, "is attached to", z)
                    # print(z, end=' ')

        # kdyz je prazdne, vytiskni .
        elif a.sum(x, y, '*').getValue() < 0.5:
            if is_tree[x][y]:
                g[y][x] = 'T'
                print("tree on position", x, y)
                # print("T", end=' ')
            else:
                g[y][x] = '.'
                print("empty on position", x, y)
                # print(".", end=' ')

for i in g:
    print(i)
