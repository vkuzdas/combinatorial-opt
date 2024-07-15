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

dirs = ['up', 'right', 'down', 'left']
a = m.addVars(n+2, n+2, dirs, vtype=g.GRB.BINARY)
M = 8
for x in range(1, n+1):
    for y in range(1, n+1):
        if not is_tree[x][y]:
            m.addConstr(a[x,y+1,'up'] == 0, name="tent can't be attached up")
            m.addConstr(a[x+1,y,'right'] == 0, name="tent can't be attached right")
            m.addConstr(a[x,y-1,'down'] == 0, name="tent can't be attached down")
            m.addConstr(a[x-1,y,'left'] == 0, name="tent can't be attached left")
        elif is_tree[x][y]:
            # m.addConstr(g.quicksum(a[x,y+1,'down'] + a[x+1,y,'left'] + a[x,y-1,'up'] + a[x-1,y,'right'] == 1),name="tent has to be attached somewhere")
            m.addConstr(a[x,y+1,'up'] + a[x+1,y,'right'] + a[x,y-1,'down'] + a[x-1,y,'left'] == 1, name="tent has to be attached somewhere")
            # no tent where tree is
            # m.addConstr(a.sum(x,y,'*') == 0, name="no tent where tree is")

        # kdyz a(xy)=1 -> M*0 >= suma, tzn suma je take tlacena do nuly (musi se rovnat aspon)
        # kdyz a(xy)=0 ->   8 >= suma
        m.addConstr( M*(1-a.sum(x,y,'*')) >=
                    a.sum(x,y+1,'*') + a.sum(x+1,y,'*') + a.sum(x,y-1,'*') + a.sum(x-1,y,'*')
                    + a.sum(x-1, y-1, '*') + a.sum(x-1, y+1, '*') + a.sum(x+1, y-1, '*') + a.sum(x+1, y+1, '*' )
                    , name="tent can be attached only once")

        # na jednom poli muze byt jen jeden strom
        m.addConstr(a.sum(x,y,'*') <= 1, name='max one tent per cell')

# PRAZDNE BUNKY ---------------------------------------
m.addConstr(a.sum(0,'*','*') == 0, name='left col empty')
m.addConstr(a.sum(n+1,'*','*') == 0, name='right col empty')
m.addConstr(a.sum('*',0,'*') == 0, name='top row empty')
m.addConstr(a.sum('*',n+1,'*') == 0, name='lower row empty')


for i in range(1,n+1):
    m.addConstr(a.sum(i, '*', '*') == c[i-1], name='tents in row')
    m.addConstr(a.sum('*', i, '*') == r[i-1], name='tents in col')

# m.addConstr(a.sum('*', '*', '*') == len(trees), name="#trees == #tents")

m.optimize()

tents = []
for x in range(1, n+1):
    for y in range(1, n+1):
        if a.sum(x,y,"*").getValue() > 0.5:
            tents.append((x,y))

visualize(n, trees, tents, r, c)


# PRINT ---------------------------------------
# for i in range(1, n+1):
#     for j in range(1, n+1):
#         for d in dirs:
#             if a[i,j,d].x > 0.5:
#                 print(str(i)+str(j)+(d[0]), end=' ')
#         # print(a[i,j,d].x, end=' ')
#     print()
# for j in range(1, n+1):
#     print(a.select('*', '*', '*'))
