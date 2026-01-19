# 🧩 Combinatorial Optimization (B4M35KO)

Coursework from the **Combinatorial Optimization** course at [CTU Prague FEE](https://fel.cvut.cz/).

The course covers mathematical optimization techniques including [Integer Linear Programming](https://en.wikipedia.org/wiki/Integer_programming), [network flows](https://en.wikipedia.org/wiki/Maximum_flow_problem), and constraint satisfaction.

## 📋 Course Topics

- Integer Linear Programming (ILP)
- Linear Programming relaxation
- [Network flows](https://en.wikipedia.org/wiki/Maximum_flow_problem) (Edmonds-Karp)
- [TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem) and subtour elimination
- Constraint satisfaction problems

## 📁 Repository Structure

| Folder | Problem | Algorithm/Technique |
|--------|---------|---------------------|
| [HW1_call_cent](kopti/HW1_call_cent/) | Call Center Scheduling | ILP with Gurobi |
| [hw2_public](kopti/hw2_public/) | Shredded Image Reconstruction | TSP formulation, subtour elimination |
| [HW3](kopti/HW3/) | Product Allocation with Bounds | Max-flow (Edmonds-Karp) |
| [02_coco](kopti/02_coco/) | Kidney Exchange Problem | Cycle cover, lazy constraints |
| [sudoku](kopti/sudoku/) | Sudoku Solver | Binary ILP |
| [cv/chess](kopti/cv/chess/) | Non-attacking Knights & Rooks | ILP with Big-M |
| [cv/tents_in_the_forest](kopti/cv/tents_in_the_forest/) | Tents Puzzle | ILP constraint modeling |
| [cv/cv5](kopti/cv/cv5/) | Circle Approximation | LP with cutting planes |

## ⚙️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3 |
| Solver | [Gurobi](https://www.gurobi.com/) |
| Visualization | Matplotlib |
| Algorithms | Edmonds-Karp, LP/ILP |

## 🚀 Usage

```bash
# Install Gurobi (requires license)
pip install gurobipy

# Run homework
python main.py input.txt output.txt
```

## 📚 References

- [B4M35KO Course Page](https://cw.fel.cvut.cz/wiki/courses/b4m35ko/)
- [Gurobi Optimization](https://www.gurobi.com/)
- [Integer Programming (Wikipedia)](https://en.wikipedia.org/wiki/Integer_programming)
- [Maximum Flow Problem](https://en.wikipedia.org/wiki/Maximum_flow_problem)
