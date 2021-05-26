# Exercise 2: Value Selection Heuristics (5 Marks)

In [heuristics.py](../heuristics.py) there are 2 value ordering heuristics. We
have implemented the first of these, `value_ordering_lex`, to get you started.
This heuristic simply returns values in the order they appear in the variable
definition when we first defined the problem. We call this the lexicographic
order:

```python
def value_ordering_lex(var: str, assignment: Dict[str, str], gamma: CSP) -> List[str]:
    """Order the values based on lexicographic order.

    In this heuristic, variable values are ordered in lexicographic order. We
    have implemented this heuristic for you. We make use of the attribute
    `gamma.current_domains` to be useful. This is a dictionary that maps a
    variable name (a string) to a set of values (a set of strings) in that
    variable's current domain.

    Parameters
    ----------
    var : str
        The name of the variable which we want to assign a value.
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    values : List[str]
        A list the values (represented a strings) in the current domain of the
        variable, sorted according to this heuristic.

    """
    # We need to explicitly convert a set to a list.
    return list(gamma.current_domains[var])
```

## The Task

We want you to implement the **Least Constraining Value** (`LCVF` from now on).
See the lectures for the precise definition. In the Russell & Norvig textbook,
this heuristic is called **MinConflict**. Intuitively, we want to pick the
value that doesn't conflict much with others. Implement this heuristic in the
function `value_ordering_lcvf` in [heuristics.py](../heuristics.py).
Break ties using lexicographic order.

## Grading Guide

Your implementation should expand a similar number of nodes to the benchmark
below. For a fair comparison, we use the default `lex` variable selection
heuristic in all of these runs. Note again how the heuristic can actually
expand even more nodes in certain cases. These results were obtained using python 3.8.5

| Instance         |     lex |    lcvf |
|------------------|---------|---------|
| sudoku_01.csp    |     316 |     257 |
| sudoku_02.csp    |   7,214 |   7,123 |
| sudoku_03.csp    |  17,257 |  17,195 |
| sudoku_04.csp    |  89,008 |  88,930 |
| sudoku_05.csp    |  20,369 |  20,303 |
| sudoku_06.csp    |   2,599 |   2,510 |
| sudoku_07.csp    |  75,446 |  75,366 |
| sudoku_08.csp    |  85,367 |  85,270 |
| sudoku_09.csp    | 193,901 | 193,814 |
| sudoku_10.csp    | 364,185 | 364,087 |
| 3_color_50_l.csp |      75 |      75 |
| 8_queens.csp     |     876 |     991 |


## What to Submit

The file `heuristics.py` with the implementation of the heuristic.

## Index

1. [Getting Started](1_getting_started.md)
2. [CSP File Format](2_csp_syntax.md)
3. [Exercise 1: Variable Selection Heuristics (10 Marks)](3_variable_selection_heuristics.md)
4. **Exercise 2: Value Selection Heuristics (5 Marks)**
5. [Exercise 3: Forward Checking (10 Marks)](5_forward_checking.md)
6. [Exercise 4: AC-3 (25 Marks)](6_ac_3.md)
7. [Exercise 5: Compiling n-ary Constraints into Binary Constraints (20 Marks)](7_compilation.md)
8. [Exercise 6: Wumpus Where Are You? (30 Marks)](8_wumpus_world.md)
9. [Wumpus World Maps Layouts](8a_map_layouts.md)
