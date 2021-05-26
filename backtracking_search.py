# COMP3620/6320 Artificial Intelligence
# The Australian National University
# Authors: COMP-3620 team
# Date:    2021

""" This file implements an iterative, stack-based backtracking search.

    It uses the given select_unassigned_variable, order_domain_values, and
    inference (constraint propagation) functions to perform the search.

    You can look in this file if you are curious about how the search algorithm
    works, but it should not be required to complete the assignment.

    ********** Do not modify any code in this file **********
"""

import sys
import time


def search(csp, initial_assignment, select_unassigned_variable,
           order_domain_values, inference):
    """ Do backtracking search on the CSP.

        Return the assignment found as a solution, the number of nodes expanded
        and the search time. If no solution can be found, None will be returned
        in place of the solution.

        (CSP, set([str]), (set([str]), CSP) -> ({str : str}, int, float)
    """

    start_time = time.time()
    assignment = dict(initial_assignment)

    # The stack will contain a list of [var, values, val_pos]
    # if values is None then this was not a decision
    stack = []

    n_expanded_nodes = 0
    while True:
        # Select the variable to be expanded
        var = select_unassigned_variable(assignment, csp)

        # Check if all variables are assigned and we therefore have a solution
        if var is None:
            print("Solved problem!")
            print("Nodes expanded:", n_expanded_nodes)
            soln_time = time.time() - start_time
            print("Time:", soln_time)
            return assignment, n_expanded_nodes, soln_time

        # Order the values for this variable
        values = order_domain_values(var, assignment, csp)

        # Push the new variable onto the stack so we can go through its values
        stack.append([var, values, 0])

        # Try and assign the values in the given order
        while True:
            var, values, pos = stack[-1]

            if pos >= len(values):
                # There are no more values, so backtrack
                stack.pop()

                # We have run out of values for the very first variable, so UNSAT!
                if not stack:
                    print("No solution!")
                    print("Nodes expanded:", n_expanded_nodes)
                    soln_time = time.time() - start_time
                    print("Time:", soln_time)
                    return None, n_expanded_nodes, soln_time

                # We are making the next decision at the backtracked level
                stack[-1][2] += 1

                # The method csp.clear_assignment() restores the domain of
                # `undo_var` to the domain before the assignment. It will also
                # delete `undo_var` from the dictionary `assignment.`
                undo_var = stack[-1][0]
                csp.clear_assignment(undo_var, assignment)
                continue

            n_expanded_nodes += 1

            val = values[pos]

            # Check if setting this value would cause a direct conflict. This
            # involves looping through all the immediate neighbours of vars. If
            # there exists at least one neighbour with an empty domain after we
            # assign val to var, then we skip this iteration.
            if csp.count_conflicts(var, val):
                stack[-1][2] += 1
                continue

            # We do not immediately conflict, so make the assignment. The
            # method csp.make_assignment() simply reduces the domain of var
            # into a singleton.
            csp.make_assignment(var, val)
            assignment[var] = val

            # Use the inference function to do constraint propagation, which will
            # possibly make more assignments or detect a conflict
            pruned_list = inference(var, assignment, csp)

            # If there is a conflict, undo the last assignment and get ready to
            # try the next one
            if pruned_list is None:
                stack[-1][2] += 1
                csp.clear_assignment(var, assignment)
                continue

            # Update the CSP with the results of the inference procedure
            csp.notify_of_inference(var, assignment, pruned_list)

            # Given our best knowledge, there is no conflict yet, so we go back
            # up to the outer loop and continue to choose a new variable
            break
