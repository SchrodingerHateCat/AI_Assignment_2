# Getting Started

Constraint Satisfaction Problems (CSPs) are a class of problems where, unlike
the previous search problems we considered in [Assignment
1](https://gitlab.cecs.anu.edu.au/comp3620/2020/comp3620-2020-assignment-1),
states have a simple representation.

CSPs determine whether a solution exists for a given constraint network. We
will assume that you are familiar with the definitions and concepts presented
in KRR lectures. We recommend that you get familiar with these before
attempting the assignment.

## The Solver

The given solver provides an implementation of Naive Backtracking. You can
check out the code in [backtracking_search.py](../backtracking_search.py). As
an example, the command

```sh
python3 solver.py -v lex -k test_problems/sudoku_01.csp
```

will solve the first of the 10 Sudoku puzzles. You should get the following
output:

```raw
$ python3 solver.py -v lex -k test_problems/sudoku_01.csp

Random Number Generator Seed: 8193
Parsing CSP file: test_problems/sudoku_01.csp
Success.
Preprocessing...
Preprocessing made 0 assignments.
Search algorithm: Backtracking
Solved problem!
Nodes expanded: 409
Time: 0.002850055694580078
Solution found.
1 5 6 | 3 2 4 | 7 9 8
3 4 9 | 1 7 8 | 2 6 5
2 7 8 | 5 6 9 | 1 3 4
---------------------
5 6 1 | 2 8 3 | 4 7 9
4 9 3 | 7 5 1 | 6 8 2
8 2 7 | 4 9 6 | 3 5 1
---------------------
6 1 5 | 9 3 2 | 8 4 7
9 3 4 | 8 1 7 | 5 2 6
7 8 2 | 6 4 5 | 9 1 3
```

The argument `-k` displays the solution as a nicely formatted Sudoku board. The
argument `-v` allows us to select which variable selection heuristic we will
use to steer backtracking. Here we select `lex`, which is the trivial heuristic
of returning variables in the order that they were declared in the input file
`test_problems/sudoku_01.csp`.

You can get the full list of all the options by specifying the `-h` flag.

```raw
$ python3 solver.py -h
usage: solver.py [-h] [-o OUTPUT] [-s SOLUTION] [-S SEARCH] [-R RNG] [-v VAR]
                 [-l VAL] [-p PRE] [-i INF] [-t MAX_STEPS] [-k]
                 INPUT

positional arguments:
  INPUT                 The path to the input CSP file.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        If given, write the grounded CSP to this file (and
                        don't solve it).
  -s SOLUTION, --solution SOLUTION
                        If given, write the satisfying assignment to this
                        file.
  -S SEARCH, --search SEARCH
                        Choose a search algorithm from [backtracking, local]
                        (default: backtracking)
  -R RNG, --seed RNG    Select a seed for the random number generator (default: 8193)
  -v VAR, --var_heuristic VAR
                        Choose a variable selection heuristic from [lex, md,
                        mrv, md-mrv, mrv-md] (default: lex)
  -l VAL, --val_heuristic VAL
                        Choose a value selection heuristic from [lex, lcvf]
                        (default: lex)
  -p PRE, --preprocessing PRE
                        Choose an inference function to use as a preprocessing
                        step before search: [arc]. If not given, no
                        preprocessing is used.
  -i INF, --inference INF
                        Choose an inference function that runs during
                        search:[forward, arc]. If not given, no inference is
                        used.
  -t MAX_STEPS, --max_steps MAX_STEPS
                        The maximum number of steps used for Local Search
                        (default: 10000)
  -k, --sudoku          Interpret the solution as Sudoku output and display it
                        in the terminal.
```

Notes:

- The `INPUT` argument (the path to the `csp` file to be solved) **always**
  needs to go last,
- In this assignment, we always use the `backtracking` algorithm. Thus you can
  ignore the `SEARCH`,`RNG` and`MAX_STEPS` options as they're only used in local
  search.
- The `-p`, `--preprocessing` option will have the solver to invoke the
  inference procedure `PRE` at the root node of the backtracking search.

## Index

1. **Getting Started**
2. [CSP File Format](2_csp_syntax.md)
3. [Exercise 1: Variable Selection Heuristics (10 Marks)](3_variable_selection_heuristics.md)
4. [Exercise 2: Value Selection Heuristics (5 Marks)](4_value_selection_heuristics.md)
5. [Exercise 3: Forward Checking (10 Marks)](5_forward_checking.md)
6. [Exercise 4: AC-3 (25 Marks)](6_ac_3.md)
7. [Exercise 5: Compiling n-ary Constraints into Binary Constraints (20 Marks)](7_compilation.md)
8. [Exercise 6: Wumpus Where Are You? (30 Marks)](8_wumpus_world.md)
9. [Wumpus World Maps Layouts](8a_map_layouts.md)
