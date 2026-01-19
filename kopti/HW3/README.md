# 📦 Product Allocation with Flow Bounds (HW3)

Solve a bounded flow problem using the [Edmonds-Karp](https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm) algorithm to allocate products to customers with lower and upper bounds.

## 📋 Problem

Given:
- $C$ customers, each with lower/upper bounds on total products
- $P$ products, each with demand to be fulfilled
- Customer-product compatibility constraints

Find a feasible allocation satisfying all bounds.

## 🧮 Formulation

Transform to standard max-flow with:
- **Source** connected to customers (capacity = upper - lower)
- **Customers** connected to compatible products (capacity = 1)
- **Products** connected to **sink** (capacity = demand)
- Handle lower bounds via demand transformation

## ⚙️ Algorithm

[Edmonds-Karp](https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm) = BFS-based Ford-Fulkerson:

```python
def edmonds_karp(graph, source, sink):
    while True:
        parent = [-1] * len(graph)
        max_capacity = find_augmenting_path_bfs(graph, source, sink, parent)
        if max_capacity == 0:
            break
        # Update flow along path
        augment_path(graph, parent, sink, max_capacity)
    return flow
```

**Time Complexity:** $O(VE^2)$

## 🚀 Usage

```bash
python main.py input.txt output.txt
```

## 📁 Input Format

```
<num_customers> <num_products>
<lower> <upper> <product_1> <product_2> ...   # Customer 1
...
<demand_product_1> <demand_product_2> ...     # Product demands
```

## 📚 References

- [Edmonds-Karp Algorithm](https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm)
- [Maximum Flow Problem](https://en.wikipedia.org/wiki/Maximum_flow_problem)
- [Flow with Lower Bounds](https://en.wikipedia.org/wiki/Maximum_flow_problem#Maximum_flow_with_lower_bounds)
