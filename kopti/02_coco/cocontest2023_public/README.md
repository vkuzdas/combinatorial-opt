# 🫀 Kidney Exchange Problem (COCO Contest 2023)

[Integer Linear Programming](https://en.wikipedia.org/wiki/Integer_programming) solution for the [Kidney Exchange Problem](https://en.wikipedia.org/wiki/Kidney_paired_donation) — finding optimal organ donation cycles.

## 📋 Problem

In kidney exchange, incompatible donor-patient pairs can swap donations in cycles:
- Patient A receives from Donor B
- Patient B receives from Donor C
- Patient C receives from Donor A

**Goal:** Find disjoint cycles maximizing total compatibility/preference scores, with cycle length limit $L$.

## 🧮 ILP Formulation

**Variables:**
- $x_{i,j} \in \{0,1\}$ — Edge from donor $i$ to patient $j$ is used
- $y_i \in \{0,1\}$ — Node $i$ participates in some cycle

**Constraints:**

1. **Flow conservation:** Each participating node has exactly one incoming and one outgoing edge:
$$\sum_j x_{i,j} = y_i, \quad \sum_j x_{j,i} = y_i$$

2. **Cycle length limit (lazy):** Cycles longer than $L$ are forbidden via callback:
$$\sum_{(i,j) \in \text{cycle}} x_{i,j} \leq |\text{cycle}| - 1$$

**Objective:**
$$\max \sum_{i,j} P_{i,j} \cdot x_{i,j}$$

where $P_{i,j}$ is the preference/compatibility score.

## ⚙️ Algorithm

Uses lazy constraint callback for subtour elimination:
1. Solve ILP relaxation
2. On integer solution, find longest cycle
3. If cycle length > $L$, add elimination constraint
4. Repeat until all cycles respect limit

```python
def my_callback(model, where):
    if where == g.GRB.Callback.MIPSOL:
        cycle = longest_cycle(selected_edges)
        if len(cycle) > L:
            model.cbLazy(sum(x[i,j] for (i,j) in cycle_edges) <= len(cycle) - 1)
```

## 🚀 Usage

```bash
python main.py public/instances/inst1.txt public/solutions/out.txt
```

## 📁 Input Format

```
<num_nodes> <num_edges> <max_cycle_length>
<src> <dst> <preference>
...
```

## 📤 Output Format

```
<total_preference>
<src1> <dst1>
<src2> <dst2>
...
```

## 📚 References

- [Kidney Paired Donation](https://en.wikipedia.org/wiki/Kidney_paired_donation)
- [Kidney Exchange Algorithms](https://en.wikipedia.org/wiki/Kidney_exchange)
- [Cycle Cover Problem](https://en.wikipedia.org/wiki/Vertex_cycle_cover)
