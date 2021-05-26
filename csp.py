# COMP3620/6320 Artificial Intelligence
# The Australian National University
# Authors: COMP-3620 team
# Date:    2021

""" This file contains a class CSP, which represents a CSP.

    You will need to look through the first part of this file to understand
    the attributes of this class that you will need to use to implement your
    heuristics and inference functions.

    The __init__ method explains these attributes.

    You will likely need: variables, neighbours, conflicts, and current_domains

    You will not need to directly modify any of these attributes.

    You will also need the method conflicts(var, val):

    This method returns the number of conflicts setting var to val would cause.

    ********** Do not modify any code in this file **********
"""

import itertools
import os
from typing import Dict, List, Set, Tuple

Variable = str
Value = str
Pair = Tuple[Variable, Value]
VarPair = Tuple[Variable, Variable]


class CSP:
    """ A CSP which we can either parse from a file, or directly add variables
        and constraints to.
    """

    def __init__(self):
        """Make a new CSP with no variables."""
        # Here variables are strings
        self.variables: List[Variable] = []

        # Each variable has a domain of possible values (these do not change throughout search)
        self.domains: Dict[Variable, List[Value]] = {}

        # Each variable has a set of neighbouring variables, which it appears in
        # constraints with
        self.neighbours: Dict[Variable, Set[Variable]] = {}

        # The conflicts graph is a dictionary that stores all conflicts. The
        # key of this dictionary is a (variable, value) pair. Let us call this
        # key X. The value of the dictionary is another dictionary, which maps
        # other variables to the values that conflict with X.
        self.conflicts: Dict[Pair, Dict[Variable, Set[Value]]] = {}
        self.conflict_weights = {}

        # A list of ground conflicts in case we want to display them
        self.ground_conflicts: List[str] = []

        # Throughout search, the domains of variables will shrink as we make
        # decisions and do inference. This starts out being the same as domains
        self.current_domains: Dict[Variable, Set[Value]] = {}

        # Whenever changes to domains we need to backtrack. You do not need to use it directly.
        self.undo_domains: Dict[Variable, Set[Pair]] = {}
        self.undo_domains[None] = set()

        # Whenever changes to assignments we need to backtrack. You do not need to use it directly.
        self.undo_assignments: Dict[Variable, Set[Variable]] = {}
        self.undo_assignments[None] = set()

    def count_conflicts(self, var: Variable, val: Value) -> int:
        """Count the constraints that would be violated by making this assignment."""

        # Basically, we loop through every neighbour of `var`. For each
        # neighbour, we ask if there is at least one value that we can assign
        # to the neighbour that doesn't conflict with `var`. If no such
        # assignment is possible, we increment `n_conflicts` by 1.
        n_conflicts = 0
        for ovar, ovals in self.conflicts[(var, val)].items():
            any_valid = False
            for oval in self.current_domains[ovar]:
                if oval not in ovals:
                    any_valid = True
                    break
            if not any_valid:
                n_conflicts += 1
        return n_conflicts

    def get_violated_constraints(self, var: Variable, val: Value) -> Set[VarPair]:
        """Return the scopes of the constraints that would be violated by making this assignment."""
        violated = set()
        for ovar, ovals in self.conflicts[(var, val)].items():
            any_valid = False
            for oval in self.current_domains[ovar]:
                if oval not in ovals:
                    any_valid = True
                    break
            if not any_valid:
                violated.add((var, ovar))
        return violated

# -------------------------------------------------------------------------------
# You should not need to look below this point unless you are interested
# -------------------------------------------------------------------------------

    def notify_of_inference(self, var, assignment, pruned_list):
        """ Notify the problem that setting the given variable caused the given
            list of (var, value) pairs to be pruned from domains and the given
            assignments to be made.

            This shrinks the current domains and saves the information so we can
            undo our decisions later.

            This method also takes a list of additional assignments made by var,
            so we can undo these later.

            (CSP, str, {str : str}, [(str, str)]) -> None
        """
        for ovar, oval in pruned_list:
            if oval not in self.current_domains[ovar]:
                raise ValueError("Error: " + oval +
                                 " not in the current domain of " + ovar)
            self.current_domains[ovar].remove(oval)
            self.undo_domains[var].add((ovar, oval))

    def make_assignment(self, var, val):
        """ Assign the given variable to the given value and save the information
            so that we can undo the decision.
            (CSP, str, str) -> None
        """
        self.undo_domains[var] = set([(var, oval)
                                      for oval in self.current_domains[var] if oval != val])
        self.undo_assignments[var] = set([var])
        self.current_domains[var] = set([val])

    def clear_assignment(self, var, assignment=None):
        """ Undo the assignment on the given variable and undo and changes to the
            domains of other variables that resulted.
            (CSP, str) -> None
        """
        for ovar, oval in self.undo_domains[var]:
            self.current_domains[ovar].add(oval)
        if assignment is not None:
            for ovar in self.undo_assignments[var]:
                del assignment[ovar]
        del self.undo_assignments[var]

    def add_variables(self, variables, domain):
        """ Add the given variables to the CSP, which all have the given domain.
            (CSP, [object], [object]) -> None
        """
        for var in variables:
            if var in self.variables:
                raise ValueError("Variable already exists: ", str(var))
            if not domain:
                raise ValueError("Empty domain")
            self.variables.append(var)
            self.domains[var] = list(domain)
            self.current_domains[var] = set(domain)

            self.neighbours[var] = set()
            for val in domain:
                self.conflicts[(var, val)] = {}

    def add_constraint(self, var0, var1, value_list):
        """ Add the given constraint to the CSP.
            The value_list is a set of positive pairs. Constraints are stored in
            the negative. So any arc not in this list will be added to the constraint
            graph. We also take the intersection of the arcs that we generate
            with any previous arcs for var0 and var1.

            (CSP, str, str, [(str, str)]) -> None
        """
        if var0 not in self.domains:
            raise ValueError("Unknown variable: " + str(var0))
        if var1 not in self.domains:
            raise ValueError("Unknown variable: " + str(var1))

        self.ground_conflicts.append((var0, var1, value_list))
        self.conflict_weights[(var0, var1)] = 1
        self.conflict_weights[(var1, var0)] = 1

        allowed_values = set([tuple(x) for x in value_list])

        for var0_val in self.domains[var0]:
            for var1_val in self.domains[var1]:
                self.conflicts[(var0, var0_val)][var1] = set()
                self.conflicts[(var1, var1_val)][var0] = set()
        for var0_val in self.domains[var0]:
            for var1_val in self.domains[var1]:
                if (var0_val, var1_val) not in allowed_values:
                    vv_pair = (var0, var0_val)
                    self.conflicts[vv_pair][var1].add(var1_val)
                    vv_pair = (var1, var1_val)
                    self.conflicts[vv_pair][var0].add(var0_val)
        self.neighbours[var0].add(var1)
        self.neighbours[var1].add(var0)

        return

    def add_inequality(self, var0, var1):
        """ Add an inequality between the given variables. Raises a value error
            if they are not defined.
            (CSP, str, str) -> None
        """
        value_list = []
        for val0 in self.domains[var0]:
            for val1 in self.domains[var1]:
                if val0 != val1:
                    value_list.append((val0, val1))
        self.add_constraint(var0, var1, value_list)

    def add_equality(self, var0, var1):
        """ Add an inequality between the given variables. Raises a value error
            if they are not defined.
            (CSP, object, object) -> None
        """
        value_list = []
        for val0 in self.domains[var0]:
            for val1 in self.domains[var1]:
                if val0 == val1:
                    value_list.append((val0, val1))
        self.add_constraint(var0, var1, value_list)

    def parse_csp_file(self, csp_file_name):
        """ Parse the given CSP file.

            This solver can handle problems with enumerated variables with finite domains.
        """
        try:
            with open(csp_file_name) as csp_file:
                for lid, line in enumerate(csp_file):
                    line = line.strip()
                    if not line or line[0] == "%":
                        continue
                    tokens = line.split()
                    if tokens[0] == "var":
                        try:
                            sep = tokens.index(":")
                        except ValueError:
                            print("Error on line", lid,
                                  "var definition missing colon")
                            return False
                        nvars = tokens[1:sep]
                        nvals = tokens[sep+1:]
                        if not nvars:
                            print("Error on line", lid,
                                  "var definition has no variables.")
                            return False
                        if not nvals:
                            print("Error on line", lid,
                                  "var definition has no values.")
                            return False
                        try:
                            self.add_variables(nvars, nvals)
                        except ValueError:
                            print(
                                "Error on line", lid, "var definition contains an already defined variable.")
                            return False

                    elif tokens[0] == "con":
                        try:
                            sep = tokens.index(":")
                        except ValueError:
                            print("Error on line", lid,
                                  "constraint definition missing colon")
                            return False
                        nvars = tokens[1:sep]
                        if not nvars:
                            print("Error on line", lid,
                                  "constraint definition has no variables.")
                            return False
                        if len(nvars) > 2:
                            print("Error on line", lid,
                                  "only binary and unary constraints allowed.")
                            return False

                        if len(nvars) == 1:
                            var = nvars[0]
                            # We do not encode unary constraints, we simply perform an
                            # implicit node consistency by shrinking the initial domains
                            # of variables
                            all_values = set()
                            values = []
                            for value in tokens[sep+1:]:
                                if value == ":":
                                    if not values:
                                        print("Error on line", lid,
                                              "badly formed constraint. Missing values.")
                                        return False
                                    if len(values) != len(nvars):
                                        print("Error on line", lid,
                                              "badly formed constraint. Wrong number of values.")
                                        return False

                                    val = values[0]
                                    if val not in self.domains[var]:
                                        print("Error on line", lid, "badly formed or",
                                              "inconsistent unary constraint. Unknown value:", val)
                                        return False
                                    all_values.add(val)
                                    values = []
                                else:
                                    values.append(value)
                            all_values.update(values)
                            if not all_values:
                                print("Error on line", lid,
                                      "badly formed constraint. Missing values.")
                                return False
                            new_domain = []
                            for val in self.domains[var]:
                                if val in all_values:
                                    new_domain.append(val)
                            self.domains[var] = new_domain
                            self.current_domains[var] = set(new_domain)
                        else:
                            all_values = []
                            values = []
                            for value in tokens[sep+1:]:
                                if value == ":":
                                    if not values:
                                        print("Error on line", lid,
                                              "badly formed constraint. Missing values.")
                                        return False
                                    if len(values) != len(nvars):
                                        print("Error on line", lid,
                                              "badly formed constraint. Wrong number of values.")
                                        return False
                                    all_values.append(values)
                                    values = []
                                else:
                                    values.append(value)
                            if not values:
                                print("Error on line", lid,
                                      "badly formed constraint. Missing values.")
                                return False
                            all_values.append(values)
                            self.add_constraint(nvars[0], nvars[1], all_values)
                    elif tokens[0] == "neq":
                        nvars = tokens[1:]
                        if len(nvars) != 2:
                            print(
                                "Error on line", lid, "badly formed neq: it needs to involve two variables exactly")
                            return False
                        for var1, var2 in itertools.combinations(nvars, 2):
                            try:
                                self.add_inequality(var1, var2)
                            except ValueError as e:
                                print("Error on line", lid, e.message)
                                return False
                    elif tokens[0] == "alldiff":
                        nvars = tokens[1:]
                        if len(nvars) < 3:
                            print("Error on line", lid, "badly formed alldiff")
                            return False
                        for var1, var2 in itertools.combinations(nvars, 2):
                            try:
                                self.add_inequality(var1, var2)
                            except ValueError as e:
                                print("Error on line", lid, e.message)
                                return False

                    elif tokens[0] == "allsame":
                        nvars = tokens[1:]
                        if len(nvars) < 2:
                            print("Error on line", lid, "badly formed allsame")
                            return False
                        for var1, var2 in itertools.combinations(nvars, 2):
                            try:
                                self.add_equality(var1, var2)
                            except ValueError as e:
                                print("Error on line", lid, e.message)
                                return False

                    else:
                        print("Error: unknown constraint on line", lid, ":", line)
                        return False

        except IOError as e:
            print("Error: could not open CSP file: ", csp_file_name)
            return False

        return True

    def write(self, out_file):
        """ Write the CSP to the given file object. To write to stdout do the
            following:
                import sys
                csp.write(sys.stdout)

            (CSP, file) -> None
        """
        for var in self.variables:
            out_file.write("var " + var + " : " +
                           " ".join(self.domains[var]) + "\n")
        out_file.write("\n")
        for var1, var2, values in self.ground_conflicts:
            out_file.write("con " + var1 + " " + var2 + " : " +
                           " : ".join([" ".join(vals) for vals in values]) + "\n")
