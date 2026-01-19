# ⛺ Tents in the Forest

ILP solution for the [Tents puzzle](https://en.wikipedia.org/wiki/Tents_%28puzzle%29) — place tents next to trees following placement rules.

## 📋 Problem

Given an $n \times n$ grid with trees:
- Each tree has exactly one tent adjacent (horizontally/vertically)
- Tents cannot be adjacent to each other (including diagonally)
- Row/column counts must match given constraints

## 🧮 ILP Formulation

**Variables:**
- $a_{x,y,d} \in \{0,1\}$ — Tent at $(x,y)$ attached in direction $d \in \{u,r,d,l\}$

**Constraints:**

1. **Each tree has exactly one attached tent:**
$$\sum_{d \in \text{neighbors}} a_{\text{neighbor},d} = 1$$

2. **No tent on tree positions:**
$$\sum_d a_{x,y,d} = 0 \quad \text{if tree at } (x,y)$$

3. **No adjacent tents (Big-M):**
$$M(1 - \sum_d a_{x,y,d}) \geq \sum_{\text{8 neighbors}} \sum_d a_{\text{neighbor},d}$$

4. **Row/column counts:**
$$\sum_x \sum_d a_{x,y,d} = r_y, \quad \sum_y \sum_d a_{x,y,d} = c_x$$

## 🚀 Usage

```bash
python main.py
```

## 📤 Output

```
  (1, 0, 1)
1 u . .
1 . T .
0 . . T
```

## 📚 References

- [Tents Puzzle (Wikipedia)](https://en.wikipedia.org/wiki/Tents_%28puzzle%29)
