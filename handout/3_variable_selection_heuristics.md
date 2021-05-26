# Exercise 1: Variable Ordering Heuristics (10 marks)

In [heuristics.py](../heuristics.py) you will find 5 functions, each
implementing a different variable ordering heuristic. All of these functions
have the form

```python
def var_ordering_heuristic(assignment: Dict[str, str], gamma: CSP) -> Optional[str]:
    """Implement a variable ordering heuristic.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
```

We have implemented the first of these functions, `next_variable_lex`, so you
have a functional CSP solver right from the start.

## The Task

We want you to implement the following variable ordering heuristics:

- The **Most Constraining Variable/Maximum Degree** heuristic (`MD` from now
  on). Here we choose the variable that is involved in as many constraints as
  possible. Implement this in the function `next_variable_md`. To test it, use
  the flag `-v md`.
- The **Most Constrained Variable/Minimum Remaining Value** heuristic (`MRV`
  from now on). Here we choose the variable with the smallest consistent
  domain. Implement this in the function `next_variable_mrv`. To test it, use
  the flag `-v mrv`.
- The `MD` heuristic, breaking ties with the `MRV` heuristic. Implement this in
  the function `next_variable_md_mrv`. To test it, use the flag `-v md-mrv`.
- The `MRV` heuristic, breaking ties with the `MD` heuristic. Implement this in
  the function `next_variable_mrv_md`. To test it, use the flag `-v mrv-md`.

Break any remaining ties using lexicographic order. See the lectures for the
precise definitions of these heuristics. Check the comments in
[heuristics.py](../heuristics.py) and [csp.py](../csp.py) for explanations
about data structures. In particular, in a CSP object `gamma`, you might want
to check out the following attributes:

- `gamma.variables` is a list of variables, where each variable is a string.
- `gamma.domains` is a dictionary that maps each variable to a list of possible
  values that we can assign to the variable.
- `gamma.neighbours` is a dictionary that maps each variable to a set of
  neighbours that have at least one constraint with that variable.
- `gamma.conflicts` and a dictionary of the conflict graph. The key of this
  dictionary is a `(variable, value)` pair. Let us call this key `X`. The
  value of the dictionary is another dictionary, which maps other
  variables to the values that conflict with `X`.

Remember these are heuristics. They don't always help, and sometimes they will
make your search much slower instead of much faster. If your heuristic does
badly on some domains, try it on others.

In the slides and textbook, constraints are grouped by the two variables they
are between, while in the code they are grouped by the (variable, value) pair
that they conflict with. In the code, we store these conflicts in a dictionary
called `conflicts`, which is an attribute inside the CSP object. Please pay
attention to this difference and ask your lab tutor if you do not understand
how the code framework works.

## Grading Guide

Your implementation should expand a similar number of nodes to the benchmark
below obtained using python 3.8.5. For a fair comparison, we use the default `lex` value selection
heuristic in all of these runs. Instances taking longer than 5 seconds are
timed out. Some results have a range due to slightly different ways in breaking
ties. Note also how heuristics don't always help in all cases.

| Instance         | lex    | md     | mrv  | md-mrv | mrv-md |
|------------------|--------|--------|------|--------|--------|
| sudoku_01.csp    | 316    | 403,276 | 231  | 37,316  | 267    |
| sudoku_02.csp    | 7,214   | -      | 284  | -      | 473    |
| sudoku_03.csp    | 17,257  | -      | 441  | -      | 261    |
| sudoku_04.csp    | 89,008  | -      | 296  | -      | 296    |
| sudoku_05.csp    | 20,369  | -      | 283  | -      | 283    |
| sudoku_06.csp    | 2,599   | -      | 298  | -      | 649    |
| sudoku_07.csp    | 75,446  | -      | 305  | -      | 1,268   |
| sudoku_08.csp    | 85,367  | -      | 2,750 | -      | 5,450   |
| sudoku_09.csp    | 193,901 | -      | 4,794 | -      | 3,264   |
| sudoku_10.csp    | 364,185 | -      | 2,438 | -      | 746    |
| 3_color_50_l.csp | 75     | 77     | 75   | 77     | 75     |
| 8_queens.csp     | 876    | 876    | 572  | 572    | 572    |



### What to Submit

The file `heuristics.py` with your implementations.

## Index

1. [Getting Started](1_getting_started.md)
2. [CSP File Format](2_csp_syntax.md)
3. **Exercise 1: Variable Selection Heuristics (10 Marks)**
4. [Exercise 2: Value Selection Heuristics (5 Marks)](4_value_selection_heuristics.md)
5. [Exercise 3: Forward Checking (10 Marks)](5_forward_checking.md)
6. [Exercise 4: AC-3 (25 Marks)](6_ac_3.md)
7. [Exercise 5: Compiling n-ary Constraints into Binary Constraints (20 Marks)](7_compilation.md)
8. [Exercise 6: Wumpus Where Are You? (30 Marks)](8_wumpus_world.md)
9. [Wumpus World Maps Layouts](8a_map_layouts.md)
