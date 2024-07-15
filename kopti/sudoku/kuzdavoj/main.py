#!/usr/bin/env python3

import gurobipy as g

# given i and j index in 9x9 grid, return all indexes of 3x3 subgrid
def get_subgrid_indices(i,j):
    i_start = i//3*3
    j_start = j//3*3
    return [(i,j) for i in range(i_start, i_start+3) for j in range(j_start, j_start+3)]


board =[
    # generate random sudoku board
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0],
]


m = g.Model("sudoku")
x = m.addVars(9, 9, 9, vtype=g.GRB.BINARY, name="x")



for i in range(9):
    for j in range(9):
        if board[i][j] != 0:
            num = board[i][j]
            m.addConstr(x[i,j,num-1] == 1)



for i in range(9):
    for j in range(9):
        #   1. Each cell must take exactly one value (sum_v x[i,j,v] = 1)
        # respektive suma na poli I,J v kazdem chlivecku musi byt 1
        m.addConstr(x.sum(i, j, '*') == 1, 'one_value_per_cell')

for i in range(9):
    for v in range(9):
        # 2. Each value is used exactly once per row (sum_i x[i,j,v] = 1)
        # mejme hodnotu V a radek I, delame soucet pres vsechny sloupce, zde musi byt soucet 1
        m.addConstr(x.sum(i, '*', v) == 1, 'uniq_in_row')

for j in range(9):
    for v in range(9):
        # 3. Each value is used exactly once per column (sum_j x[i,j,v] = 1)
        ## mejme hodnotu V, a sloupec J, delame soucet pres vsechny radky, zde musi byt soucet 1
        m.addConstr(x.sum('*', j, v) == 1, 'uniq_in_col')

coords = [0,3,6]

for row in coords:
    for col in coords:
        for num in range(9):
            m.addConstr(
                g.quicksum(
                x[r+row, 0+col, num] +
                x[r+row, 1+col, num] +
                x[r+row, 2+col, num] for r in range(3)) == 1)

    # toto omezuj prvni subgrid aby se neopakovala jednicka
    # num = 1
    # m.addConstr(x[0, 0, num] + x[0, 1, num] + x[0, 2, num] +
    #             x[1, 0, num] + x[1, 1, num] + x[1, 2, num] +
    #             x[2, 0, num] + x[2, 1, num] + x[2, 2, num] == 1)





m.optimize()

for row in board:
    print(row)


for i in range(9):
    for j in range(9):
        for k in range(9):
            if x[i,j,k].X > 0.5:
                if board[i][j] == 0:
                    board[i][j] = k+1
                    # print(k+1, end=' ')
                    break
                # else:
                    # print('err, bord is not empty in pos', i, j)

print()
for row in board:
    print(row)
