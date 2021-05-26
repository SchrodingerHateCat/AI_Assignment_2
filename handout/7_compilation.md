# Exercise 5: Compiling n-ary constraints into binary constraints (20 Marks)

## The Task

We will try to solve the following exercise from the Russell & Norvig book
(Exercise **6.6** in the third edition):

```raw
Show how a single ternary constraint such as "A + B = C" can be turned into three
binary constraints by using an auxiliary variable. You may assume finite domains.
(Hint: Consider a new variable that takes on values that are pairs of other values,
and consider constraints such as "X is the first element of the pair Y"). Next,
show how constraints with more than three variables can be treated similarly.
Finally, show how unary constraints can be eliminated by altering the domains
of variables. This completes the demonstration that any CSP can be transformed
into a CSP with only binary constraints.
```

Alternatively, you can just ask StackOverflow. Somebody made the right question
[there already](https://stackoverflow.com/q/19261183), and the winning answer
pretty much sums it up. In the comment under the question there is a link to an
old but reliable explanation of two procedures for this.

Instead of modifying the solver code, we want you to implement this stuff in a
separate script, called [n_to_bin.py](../n_to_bin.py) that can
import from the module [csp.py](../csp.py) anything it needs. We
have implemented for you the basic skeleton of the program, namely, processing
command line arguments and providing you with a comfortable environment to do
your own thing.

The output of `n_to_bin.py` needs to be a file that can be parsed and processed
by the provided solver **without modifications to** `csp.py`. We will test
your code with the problems you can find inside the folder `nary_problems`.
Note that in these problems we extend the syntax of our language to describe
constraint networks allowing for n-ary constraints.

Your compiler should meet the following requirements:

1. Your compiler doesn't crash on any of the example problems we provide in the
   folder `nary_problems`.
2. The compilation procedure runs in a reasonable time (in less than _5_
   minutes for the bigger instances).
3. The output `.csp` file can be correctly parsed by the solver.
4. The output of the compilation procedure is **sound** and **complete**: the
   set of solutions in the original constraint network needs to be
   **preserved**.
5. When combining values of several variables to build the set of values of any
   new variables introduced by the compilation scheme, you should use
   characters that do not confuse the (very basic) parser in
   [csp.py](../csp.py).
6. You don't need to worry about supporting `neq`, `alldiff`, and `allsame`
   constraints.

To get you started, we have implemented a function to read and parse a n-ary
CSP file:

```python
variables, constraints = parse_nary_file(input_path)
```

See the docstrings in the `parse_nary_file` for more information about the
data structures.

Once you have finished the your implementation, the following command
should generate a binarised CSP file in `nary_problems/binarised_03.csp`:

```sh
python3 n_to_bin.py --input nary_problems/linear_03.csp --output nary_problems/binarised_03.csp
```

If it is not possible to do the conversion, for example because a variable ends
up with an empty domain, your compiler should print out the message
`Unsatisfiable constraints` and then exit. Note that when solving this
question, you cannot import anything from `reference_n_to_bin`. We provide
`reference_n_to_bin` so that you can solve Exercise 6 without first needing to
solve Exercise 5 correctly. See the next exercise for more information.

Finally, note that if we have duplicate binary constraints, the solver will
only encode the last one.

## What to Submit

The file `n_to_bin.py` containing the implementation of the compilation
procedure.

## Index

1. [Getting Started](1_getting_started.md)
2. [CSP File Format](2_csp_syntax.md)
3. [Exercise 1: Variable Selection Heuristics (10 Marks)](3_variable_selection_heuristics.md)
4. [Exercise 2: Value Selection Heuristics (5 Marks)](4_value_selection_heuristics.md)
5. [Exercise 3: Forward Checking (10 Marks)](5_forward_checking.md)
6. [Exercise 4: AC-3 (25 Marks)](6_ac_3.md)
7. **Exercise 5: Compiling n-ary Constraints into Binary Constraints (20 Marks)**
8. [Exercise 6: Wumpus Where Are You? (30 Marks)](8_wumpus_world.md)
9. [Wumpus World Maps Layouts](8a_map_layouts.md)
