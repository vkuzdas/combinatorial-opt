# 📞 Call Center Scheduling (HW1)

[Integer Linear Programming](https://en.wikipedia.org/wiki/Integer_programming) solution for optimal shift scheduling in a 24-hour call center.

## 📋 Problem

Given hourly demand for operators over 24 hours, find the optimal number of operators to start each hour. Each operator works an **8-hour shift**.

**Objective:** Minimize total deviation from demand.

## 🧮 Formulation

**Variables:**
- $x_i$ — Number of operators starting at hour $i$
- $z_i$ — Absolute deviation from demand at hour $i$

**Constraints:**
- Active operators at hour $i$ = sum of those who started in last 8 hours
- $z_i \geq |demand_i - active_i|$ (linearized with two constraints)

**Objective:**
$$\min \sum_{i=0}^{23} z_i$$

## 🚀 Usage

```bash
python main.py instances/instance1.txt solutions/out.txt
```

## 📁 Input Format

Space-separated demand values for 24 hours:
```
5 3 2 2 3 5 8 12 15 18 20 22 20 18 15 12 10 8 6 5 4 3 2 2
```

## 📤 Output Format

```
<total_deviation>
<operators_starting_hour_0> <operators_starting_hour_1> ... <operators_starting_hour_23>
```
