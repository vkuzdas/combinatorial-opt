# 🖼️ Shredded Image Reconstruction (HW2)

Reconstruct a shredded image by finding optimal stripe ordering using [TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem) formulation with subtour elimination.

## 📋 Problem

Given vertical stripes of a shredded image, find the ordering that minimizes color difference between adjacent stripe edges.

## 🧮 Formulation

Models the problem as **Asymmetric TSP**:
- Each stripe is a node
- Edge weight = RGB color difference between adjacent edges
- Add dummy node with zero-cost edges to allow open path

**Subtour Elimination:** Uses lazy callbacks to add constraints when cycles shorter than full tour are found.

## ⚙️ Algorithm

1. Build distance matrix from RGB edge differences
2. Solve TSP relaxation
3. On integer solution, check for subtours
4. Add subtour elimination constraints via callback
5. Repeat until Hamiltonian path found

```python
def my_callback(model, where):
    if where == g.GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(x)
        cycle = shortest_cycle(selected_edges)
        if len(cycle) < nodes:
            model.cbLazy(...)  # Add subtour elimination
```

## 🚀 Usage

```bash
python main.py public/instances/cat_part.txt output.txt
```

## 📁 Input Format

```
<num_stripes> <stripe_width> <stripe_height>
<RGB values for stripe 1>
<RGB values for stripe 2>
...
```

## 📚 References

- [Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
- [Subtour elimination](https://en.wikipedia.org/wiki/Travelling_salesman_problem#Integer_linear_programming_formulations)
