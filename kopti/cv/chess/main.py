#!/usr/bin/env python3
import sys

import gurobipy as g


if __name__ == '__main__':

    inFile, outFile = sys.argv[1:]
    file = open(inFile, 'r')
    # first line is number of following lines
    n = int(file.readline())
    rooks = []
    for i in range(n):
        chess_pos = file.readline().split()[0]
        x = ord(chess_pos[0])-ord('a')+2
        y = int(chess_pos[1])+1
        rooks.append((x,y))





    m = g.Model('chess')

    # abychom neresili edge cases, roztahneme sachonici
    # o 2 policka na kazde strane
    dim = 8+4
    # Create variables
    k = m.addVars(dim, dim, vtype=g.GRB.BINARY, name='horse')

    # radek falsu o dim bunkach
    # dim-krat radek falsu
    is_rook = [ [False for _ in range(dim)]  for _ in range(dim)  ]

    for x, y in rooks:
        # SWAPPED X/Y
        is_rook[y][x] = True
        # ve sloupci a radku kde stoji vez nesmi byt kun
        m.addConstr(k.sum(y, '*') == 0, name='no_rook_threat')
        m.addConstr(k.sum('*', x) == 0, name='no_rook_threat')



    # Create constraints

    M = 8
    for i in range(2, dim-2):
        for j in range(2, dim-2):
            if is_rook[i][j]:
                # pokud je na policku vez, nesmi byt na sousednich polickach kun
                # m.addConstr(k.sum(i,'*') == 0, name='no_rook_threat')
                # m.addConstr(k.sum('*',i) == 0, name='no_rook_threat')
                continue
            else:
                # kdyz je na policku kun, nesmi ohrozovat jineho kone
                # tj. kdyz bude na policku [i,j] kun, potom M*(1-k) se bude rovnat nule (protoze k=1)
                # tudiz bude contraint vypadat 0 >= k[i-2,j-1] + k[i-2,j+1] + ....
                # a tim jsme zakazali aby na okolnich polich stal kun (suma bin promennych v okoli musi byt 0)
                # na druhou stranu pokud na policku [i,j] neni kun, tak M*(1-k) se bude rovnat M protoze M*(1-0)=M=8
                # tudiz bude contraint vypadat 8 >= k[i-2,j-1] + k[i-2,j+1] + ....
                # tim jsme vlastne nic nezakazali, suma binarnich promennych na polickach muze byt do 8
                m.addConstr(M*(1-k[i,j]) >=
                            k[i-2,j-1] + k[i-2,j+1]
                            + k[i-1,j+2] + k[i+1,j+2]
                            + k[i+2,j+1] + k[i+2,j-1]
                            + k[i-1,j-2] + k[i+1,j-2], name='no_horse_threat')


    # board jsme rozsirili o 2 policka na kazde strane
    # nechceme ale aby tam stal kun
    m.addConstr(k.sum(0, '*') == 0, 'empty_edges')
    m.addConstr(k.sum(1, '*') == 0, 'empty_edges')
    m.addConstr(k.sum(dim-1, '*') == 0, 'empty_edges')
    m.addConstr(k.sum(dim-2, '*') == 0, 'empty_edges')
    m.addConstr(k.sum('*', 0) == 0, 'empty_edges')
    m.addConstr(k.sum('*', 1) == 0, 'empty_edges')
    m.addConstr(k.sum('*', dim-1) == 0, 'empty_edges')
    m.addConstr(k.sum('*', dim-2) == 0, 'empty_edges')

    m.setObjective(g.quicksum(k[i,j] for i in range(2, dim-2) for j in range(2, dim-2)), g.GRB.MAXIMIZE)

    m.optimize()

    board = [['_' for _ in range(dim)] for _ in range(dim)]
    for i in range(2, dim-2):
        for j in range(2, dim-2):
            if is_rook[i][j]:
                board[i][j] = 'T'
                # print('T', end=' ')
                continue
            if k[i,j].x == 1:
                board[i][j] = 'H'
                # print('H', end=' ')
                continue
            else:
                # print('.', end=' ')
                continue
        print()

    res = []
    for i in range(2, dim-2):
        for j in range(2, dim-2):
            if board[i][j] == 'H':
                res.append((chr(j-2+ord('a')),i-1))
            print(board[i][j], end=' ')
        print()


    print(len(res))
    for tup in res:
        print(tup[0]+str(tup[1]))

    f = open(outFile, 'w')
    f.write(str(len(res)))
    for tup in res:
        # write on each line
        f.write('\n')
        f.write(tup[0]+str(tup[1]))
    f.close()
