# CSP File Format

The solver can handle Constraint Networks where the variables have associated
finite domains. It allows both binary and unary constraints as well as
`alldiff` and `allsame` constraints. A special type of binary constraint,
`neq`, allows the modeler to specify inequality constraints with little hassle.

## Format

### Comments

Lines starting with the character `%` are ignored by the parser.

### Variables

Lines starting with `var` define the variables and their domains. For example:

```raw
var QLD NSW VIC ACT SA : red green blue
```

will create the variables `QLD`, `NSW`, `VIC`, `ACT` and `SA`, and give them
all the same domain, the set `{red, green, blue}`. Note that an empty space
before and after `:` is required.

### Binary Constraints

Arbitrary binary constraints are encoded in one single line as follows:

```raw
con WA NT : red green : red blue : green red : green blue : blue red : blue green
```

corresponding to the relation:

```math
\begin{aligned}
    C_{\text{WA},\text{NT}} = \{ &(\text{red}, \text{green}), (\text{red}, \text{blue}), (\text{green}, \text{red}), \\
     &(\text{green}, \text{blue}), (\text{blue}, \text{red}), (\text{blue}, \text{green}) \}
\end{aligned}
```

### Inequality Constraints

Inequality constraints are given in one single line as well:

```raw
neq WA NT
```

which corresponds to the same relation as above:

```math
\begin{aligned}
    C_{\text{WA},\text{NT}} = \{ &(\text{red}, \text{green}), (\text{red}, \text{blue}), (\text{green}, \text{red}), \\
     &(\text{green}, \text{blue}), (\text{blue}, \text{red}), (\text{blue}, \text{green}) \}
\end{aligned}
```

Note how the inequality constraint allows us to rewrite certain binary
constraints in a more concise way.

### Unary Constraints

Unary constraints are encoded similarly to binary constraints:

```raw
con NT : red : blue
```

This constraint restricts the domain of the variable `NT` to have either the
values `red` or `blue`. Note that unary constraints are compiled away by the
solver by modifying the domains of the variables affected and setting values
in the initial assignment.

### Higher-order Constraints

The solver supports two kinds of higher-order constraints featuring more than
two variables in their scopes. These are internally compiled into \$`O( n^2 )`$
binary constraints, where $`n`\$ is the number of variables in the scope of the
higher-order constraint.

The `alldiff` constraint indicates that all of the variables in the scope must
have different values. For example, if we want `ACT`, `NSW` and `SA` to all
have different colours, we can use the constraint:

```raw
alldiff ACT NSW SA
```

The `allsame` constraint indicates that all of the variables in the scope must
have the same value. For example, if we want `ACT`, `NSW` and `SA` to all share
the same colour, we can use the constraint:

```raw
allsame ACT NSW WA
```

As with unary and binary constraints, only one constraint can be specified per
line.

## Index

1. [Getting Started](1_getting_started.md)
2. **CSP File Format**
3. [Exercise 1: Variable Selection Heuristics (10 Marks)](3_variable_selection_heuristics.md)
4. [Exercise 2: Value Selection Heuristics (5 Marks)](4_value_selection_heuristics.md)
5. [Exercise 3: Forward Checking (10 Marks)](5_forward_checking.md)
6. [Exercise 4: AC-3 (25 Marks)](6_ac_3.md)
7. [Exercise 5: Compiling n-ary Constraints into Binary Constraints (20 Marks)](7_compilation.md)
8. [Exercise 6: Wumpus Where Are You? (30 Marks)](8_wumpus_world.md)
9. [Wumpus World Maps Layouts](8a_map_layouts.md)
