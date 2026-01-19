# 🔢 Sudoku Solver

[Integer Linear Programming](https://en.wikipedia.org/wiki/Integer_programming) solver for [Sudoku](https://en.wikipedia.org/wiki/Sudoku) puzzles using binary decision variables.

## 📋 Problem

Fill a 9×9 grid so that each row, column, and 3×3 subgrid contains digits 1-9 exactly once.

## 🧮 ILP Formulation

**Variables:**
- $x_{i,j,v} \in \{0,1\}$ — Cell $(i,j)$ contains value $v$

**Constraints:**

1. **One value per cell:**
$$\sum_{v=1}^{9} x_{i,j,v} = 1 \quad \forall i,j$$

2. **Unique in row:**
$$\sum_{j=1}^{9} x_{i,j,v} = 1 \quad \forall i,v$$

3. **Unique in column:**
$$\sum_{i=1}^{9} x_{i,j,v} = 1 \quad \forall j,v$$

4. **Unique in 3×3 subgrid:**
$$\sum_{i \in S_r} \sum_{j \in S_c} x_{i,j,v} = 1 \quad \forall v, \forall \text{ subgrids}$$

5. **Given clues:**
$$x_{i,j,v} = 1 \quad \text{if cell } (i,j) \text{ is given value } v$$

## 🚀 Usage

```bash
python main.py
```

Edit the `board` variable in `main.py` to solve different puzzles (0 = empty cell).

## 📤 Output

```
[5, 3, 4, 6, 7, 8, 9, 1, 2]
[6, 7, 2, 1, 9, 5, 3, 4, 8]
...
```

## 📚 References

- [Sudoku (Wikipedia)](https://en.wikipedia.org/wiki/Sudoku)
- [Sudoku as ILP](https://www.gurobi.com/documentation/current/examples/sudoku_py.html)
