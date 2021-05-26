# Exercise 6: Wumpus Test Maps

Test case maps. Notations:

- `B` means the agent has been here and can feel a breeze.
- `S` means the agent has been here and can feel a stench.
- `O` means the agent has been here but can't feel anything.
- `A` indicates the agent's current position.

Test Case 1: 1 Wumpus, 3 Pits

```raw
|     |     |     |     |
| --- | --- | --- | --- |
|     |     |     |     |
| --- | --- | --- | --- |
| BA  |     |     |     |
| --- | --- | --- | --- |
| O   | B   |     |     |
```

Test Case 2: 1 Wumpus, 2 Pits

```raw
|     |     |     |
| --- | --- | --- |
| SA  |     |     |
| --- | --- | --- |
| O   | BS  |     |
| --- | --- | --- |
| O   | B   |     |
```

Test Case 3: 1 Pit, 1 Wumpus

```raw
|     |     |     |
| --- | --- | --- |
| B   |     |     |
| --- | --- | --- |
| OA  |     |     |
```

Test Case 4: 1 Wumpus, 2 Pits

```raw
|     |     |     |     |
| --- | --- | --- | --- |
| BA  |     |     |     |
| --- | --- | --- | --- |
| O   | BS  |     |     |
| --- | --- | --- | --- |
| O   | O   | S   |     |
```

Test Case 5: 2 Wumpus, 0 Pits

```raw
|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|     |     |     | S   |     |
| --- | --- | --- | --- | --- |
|     | S   | O   | O   | SA  |
| --- | --- | --- | --- | --- |
|     |     |     |     |     |
```

Test Case 6: 1 Wumpus, 2 Pits

```raw
|     |     |     |     |
| --- | --- | --- | --- |
|     | BS  | O   |     |
| --- | --- | --- | --- |
|     |     | BSA |     |
| --- | --- | --- | --- |
|     | BS  |     |     |
```

Test Case 7: 2 Wumpuses, 1 pit

```raw
|     |     |     |     |
| --- | --- | --- | --- |
| S   |     |     |     |
| --- | --- | --- | --- |
| O   | S   |     |     |
| --- | --- | --- | --- |
| O   | O   | SA  |     |
```

Test Case 8: 1 Wumpus, 2 Pits


```raw
|     |     |     |     |
| --- | --- | --- | --- |
| B   |     |     |     |
| --- | --- | --- | --- |
| O   | BS  |     |     |
| --- | --- | --- | --- |
| O   | O   | SA  |     |
```

Test Case 10: 1 Wumpus, 1 Pit

```raw
|     |     |     |
| --- | --- | --- |
| B   |     |     |
| --- | --- | --- |
| O   | SA  |     |
```

Test Case 13: 1 Wumpus, 2 Pits

```raw
|     |     |     |     |
| --- | --- | --- | --- |
|     |     |     |     |
| --- | --- | --- | --- |
| B   | BA  |     |     |
| --- | --- | --- | --- |
| O   | O   | B   |     |
```

## Index

1. [Getting Started](1_getting_started.md)
2. [CSP File Format](2_csp_syntax.md)
3. [Exercise 1: Variable Selection Heuristics (10 Marks)](3_variable_selection_heuristics.md)
4. [Exercise 2: Value Selection Heuristics (5 Marks)](4_value_selection_heuristics.md)
5. [Exercise 3: Forward Checking (10 Marks)](5_forward_checking.md)
6. [Exercise 4: AC-3 (25 Marks)](6_ac_3.md)
7. [Exercise 5: Compiling n-ary Constraints into Binary Constraints (20 Marks)](7_compilation.md)
8. [Exercise 6: Wumpus Where Are You? (30 Marks)](8_wumpus_world.md)
9. **Wumpus World Maps Layouts**
