# Exercise 6: Wumpus Where Are You? (30 Marks)

In this final exercise we want you to go the extra mile and put together a more
interesting application of the algorithms you've been implementing in the first
exercises.

The task is to write a program that takes observations (percepts) gathered by
the Wumpus World agent and an action, and constructs a CSP answering the
question: Is it safe to do the action given what the agent has learnt so far?
Here "safe" means that it is impossible for the move to take the agent to the
same square as a pit or a wumpus.

The knowledge the agent has collected (or had from the beginning) comes in a
JSON document that contains the particular details of an instance of Wumpus
World (size, number of wumpuses, pits), as well as the list of percepts
collected (observations) by the agent as a result of the agent doing a set of
actions while we weren't looking. On the basis of this Knowledge Base, we want
to assess whether the next action to perform by the agent - specified manually
via the command line - is safe (that is, the cell the action takes the agent to
won't contain a wumpus or a pit). There are four possible actions: `north`,
`south`, `east`, and `west`.

The input to your program is a JSON file describing the Wumpus World. The file
[example.json](../wumpus_maps/example.json) encodes the example discussed in
the KRR lectures. Have a look the comments in that file.

We have further simplified the Wumpus World by removing from the agent the
ability to shoot arrows at anything, since we have learnt that wumpuses are an
endangered species. There is no gold either unfortunately.

The script `wumpus2csp.py` provides you with basic functionality to get you
started. Given a command, say:

```sh
python3 wumpus2csp.py --input wumpus_maps/big/wumpus_01.json --action north --output wumpus_outputs
```

your script will need to output two files inside the `wumpus_outputs` folder:

1. A binarized CSP file called `wumpus_01_north_a.csp`.
2. A binarized CSP file called `wumpus_01_north_b.csp`.

Note that the `--input` parameter requires the file-path to a Wumpus world scenario. From the base directory of this assignment, these file-paths will look like `wumpus_maps/big/wumpus_01.json`, `wumpus_maps/small/wumpus_02.json`, etc. **Do not hard code the file-paths!** We will be using a different directory structure to you!

You will need to make sure that the two CSPs that your code generates satisfy all branches of the following decision tree:

![decision tree](images/decision.png)

In other words:

- If `wumpus_01_north_a.csp` does not have a solution, then it must be safe
  to go north.
- If `wumpus_01_north_b.csp` does not have a solution, then it must NOT be
  safe to go north.
- If both CSPs have a solution, then it is uncertain whether going north is
  safe or not.
- It is not possible for both CSPs to not have a solution (i.e. a path can't be
  both safe and unsafe at the same time).

Remember to follow the naming convention when creating the output CSP. The
format is `<scenario>_<action>_<target>.csp`, where

- `scenario` can be one of: `wumpus_01`, `wumpus_02`, `wumpus_03`, `wumpus_04`,
  `wumpus_05`, `wumpus_06`, `wumpus_07`, `wumpus_08`, `wumpus_10`, `wumpus_13`.
- `action` can be one of: `north`, `south`, `east`, `west`.
- `target` can be one of: `a`, `b`.

You also need to do a experimental analysis to determine what are the best
settings of our solver for the CSPs you generate. Write up the report in a PDF
file called `experiments.pdf`. In the report, also describe the approach you
have taken in detail. You might want to create a script `run_experiments.py` or
`run_experiments.sh` that would allow us to replicate your experimental
results.

We leave it to you to structure this report mostly as you wish, but its central
element should be a table showing how the combinations of settings you tested
worked on each of the wumpus world instances you considered. You are allowed to
come up with more interesting instances as well.

Your code must not crash and the generated CSPs need to be encoded into the CSP
syntax supported by the solver. If you have n-ary constraints, you can use the
compiler you wrote in Exercise 5 to first convert them into binary constraints.
Alternatively, if you are unsure about your implementation, you can use our
prebuilt nary-to-binary compiler. To use it, you simply need to import the
`convert` function from `reference_n_to_bin`. For example, the following code
will convert `wumpus_outputs/wumpus_02_north_a.csp` into a binarised CSP
and overwrites the original file (specify a different second parameter if you
don't want to overwrite):

```python
from reference_n_to_bin import convert
convert('wumpus_outputs/wumpus_02_north_a.csp', 'wumpus_outputs/wumpus_02_north_a.csp')
```

Note that our `reference_n_to_bin` does not support `neq`, `alldiff`, and
`allsame` constraints. Also note that our `reference_n_to_bin` will raise an
error and output `Unsatisfiable constraints` if any of the generated domains
are empty when compiling to binary. If you will output such a n-ary csp, then
catch that error and return a toy binary csp that will be unsatisfiable.
Finally, if your CSP is already in binary format, do not use the converter
to do any further conversion.

## Wumpus Maps

We provide you with 7 Wumpus maps. Click [here](8a_map_layouts.md) to see the
layout of all the maps. During marking, your program will be tested on other
maps, so it's important that you don't hard-code anything. In these maps, the
origin (1, 1) starts at the bottom left. If the agent takes one step to the
east, we'll move to (2, 1). If the agent takes one step to the north, we'll
move to (1, 2). As an example, let's check out the second map `wumpus_02.json`
with 1 wumpus and 2 pits:

```raw
|     |     |     |
| --- | --- | --- |
| SA  |     |     |
| --- | --- | --- |
| O   | BS  |     |
| --- | --- | --- |
| O   | B   |     |
```

where:

- `B` means the agent has been here and can feel a breeze.
- `S` means the agent has been here and can feel a stench.
- `O` means the agent has been here but can't feel anything.
- `A` indicates the agent's current position.

The agent starts at (1, 1), then moves around and finally ends up at (1, 3).
Assume that the last observation in the json file is the agent's current
position. At (1, 3), the agent infers that the wumpus `w` must be at (2,
3), and the position (1, 4) must be safe (indicated with `y`):

```raw
| y   |     |     |
| --- | --- | --- |
| SA  | w   |     |
| --- | --- | --- |
| O   | BS  |     |
| --- | --- | --- |
| O   | B   |     |
```

Thus if we run:

```sh
python3 wumpus2csp.py --input wumpus_maps/small/wumpus_02.json --action north --output wumpus_outputs
# This should produce two binarized CSP files:
#   wumpus_outputs/wumpus_02_north_a.csp
#   wumpus_outputs/wumpus_02_north_b.csp

# Let's try going north.
python3 solver.py wumpus_outputs/wumpus_02_north_b.csp
# The solver should return a solution.
python3 solver.py wumpus_outputs/wumpus_02_north_a.csp
# The sovler should return "There is no solution!". Thus going north is safe.

# Let's now try going east.
python3 wumpus2csp.py --input wumpus_maps/small/wumpus_02.json --action east
python3 solver.py wumpus_outputs/wumpus_02_east_a.csp
# The solver should return a solution.
python3 solver.py wumpus_outputs/wumpus_02_east_b.csp
# The sovler should return "There is no solution!". Thus going east is NOT safe.
```

Note that if you look inside each json file, we give you what the correct
outcome for each move is (the first four attributes). For example for
`wumpus_02`, from the current position (1, 3), moving north is safe, while
moving east is unsafe, Moving south is trivially safe (since we were there in
the previous step). Moving west is invalid since we can't go outside the board.
In your implementation, you can assume that the agent stays where it is if an
invalid move is provided.


## Other Implementation Requirements

1. This exercise is complex, but can be solved with relatively few lines of code. **We will only look at the first 400 lines of code!** Subsequently, you will only receive marks for those lines!
2. Given a Wumpus world layout and a single action, the cumulative time to call your code and solve the ensuing 2 CSP's should:
    - use no more than 2GB RAM,
    - generate CSP text files no larger than 10 MB (1048576 bytes) each,
    - take no longer than 5 minutes in total, that is, to generate both files and solve both of the (we will test your code on a regular machine, so if you are able to solve the Wumpus scenario in under 5 minutes you should be safe).
3. **Commenting is not optional for this exercise.** This exercise is particularly open-ended, and for us to easily understand your code, you must put some time and work into adding well-thought-out comments that explain your approach. **5/30 marks for this exercise are reserved for good commenting**.


## What To Submit

The files:

- `wumpus2csp.py`
- `experiments.pdf`
- `run_experiments.py` or `run_experiments.sh`
- Any additional wumpus instances you have used in your experimental analysis.


## Index

1. [Getting Started](1_getting_started.md)
2. [CSP File Format](2_csp_syntax.md)
3. [Exercise 1: Variable Selection Heuristics (10 Marks)](3_variable_selection_heuristics.md)
4. [Exercise 2: Value Selection Heuristics (5 Marks)](4_value_selection_heuristics.md)
5. [Exercise 3: Forward Checking (10 Marks)](5_forward_checking.md)
6. [Exercise 4: AC-3 (25 Marks)](6_ac_3.md)
7. [Exercise 5: Compiling n-ary Constraints into Binary Constraints (20 Marks)](7_compilation.md)
8. **Exercise 6: Wumpus Where Are You? (30 Marks)**
9. [Wumpus World Maps Layouts](8a_map_layouts.md)
