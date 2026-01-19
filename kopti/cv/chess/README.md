# ♞ Non-Attacking Knights (Chess)

Place maximum knights on a chessboard such that no two knights attack each other, with some squares occupied by rooks.

## 📋 Problem

Given rook positions on an 8×8 board:
- Knights cannot be placed on rook rows/columns
- No two knights can attack each other (L-shaped move)

**Objective:** Maximize number of placed knights.

## 🧮 ILP Formulation

**Variables:**
- $k_{i,j} \in \{0,1\}$ — Knight placed at position $(i,j)$

**Constraints:**

1. **No knight on rook rows/columns:**
$$\sum_j k_{i,j} = 0 \quad \text{if row } i \text{ has a rook}$$

2. **No attacking knights (Big-M method):**
$$M(1-k_{i,j}) \geq \sum_{\text{knight moves}} k_{\text{target}}$$

The Big-M constraint means: if a knight is at $(i,j)$, then all 8 knight-move targets must be empty.

## 🚀 Usage

```bash
python main.py instances/public1.txt solutions/out.txt
```

## 📁 Input Format

```
<num_rooks>
a1
c3
...
```

## 📚 References

- [Knight's tour](https://en.wikipedia.org/wiki/Knight%27s_tour)
- [Big-M method](https://en.wikipedia.org/wiki/Big_M_method)
