# ⭕ Circle Approximation with Cutting Planes

[Linear Programming](https://en.wikipedia.org/wiki/Linear_programming) optimization over a circular feasible region using iterative [cutting plane](https://en.wikipedia.org/wiki/Cutting-plane_method) method.

## 📋 Problem

Optimize a linear objective over a circular constraint:
$$\min \; c_1 x + c_2 y$$
$$\text{s.t.} \; (x - a)^2 + (y - b)^2 \leq r^2$$

Since the constraint is non-linear, we approximate it with tangent halfspaces.

## 🧮 Algorithm

1. Start with a coarse polyhedral approximation of the circle
2. Solve LP relaxation
3. If solution is outside circle, add tangent line as cutting plane
4. Repeat until solution is feasible

```python
def create_tangent_line(circle_center, solution):
    # Tangent at point on circle closest to solution
    vector = normalize(solution - circle_center)
    base_point = circle_center + radius * vector
    return Line(base_point, perpendicular(vector))
```

## ✨ Features

- Interactive matplotlib visualization
- Step-by-step cutting plane addition
- Halfspace intersection computation with SciPy

## 🚀 Usage

```bash
python main.py
```

Click the "Next Step" button to add cutting planes iteratively.

## 📚 References

- [Cutting-plane method](https://en.wikipedia.org/wiki/Cutting-plane_method)
- [Linear Programming](https://en.wikipedia.org/wiki/Linear_programming)
