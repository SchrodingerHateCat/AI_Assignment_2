"""Inference functions used with backtracking search.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: COMP-3620 team
Date:    2021

Student Details
---------------
Student Name:
Student Number:
Date:
"""

import collections
from typing import Callable, Dict, List, Optional, Tuple
import copy
from csp import CSP

Assignment = Dict[str, str]
Pruned = List[Tuple[str, str]]


def forward_checking(var: str, assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    """Implement the forward checking inference procedure.

    Parameters
    ----------
    var : str
        The name of the variable which has just been assigned.
    assignment : Dict[str, str]
        A Python dictionary of the current assignment. The dictionary maps
        variable names to values. The function cannot change anything in
        `assignment`.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution. The function cannot change
        anything in `gamma`.

    Returns
    -------
    pruned_list : Optional[Pruned]
        In the case that the algorithm detects a conflict, the assignment and
        CSP should remain unchanged and the function should return None.

        Otherwise, the algorithm should return a pruned_list, which is a list
        of (variable, value) pairs that will be pruned out of the domains of
        the variables in the problem. Think of this as the "edits" that are
        required to be done on the variable domains.

    """
    # *** YOUR CODE HERE ***
    #raise NotImplementedError("Forward Checking hasn't been implemented!")
    output = []
    if gamma.count_conflicts(var, assignment[var]) > 0:
        return None
    
    for neighbour in gamma.neighbours[var]:
        if assignment[var] in gamma.current_domains[neighbour]:
            output.append(([neighbour,assignment[var]]))
    return output
        


def arc_consistency(var: Optional[str], assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    """Implement the AC-3 inference procedure.

    Parameters
    ----------
    var : Optional[str]
        The name of the variable which has just been assigned. In the case that
        AC-3 is used for preprocessing, `var` will be `None`.
    assignment : Dict[str, str]
        A Python dictionary of the current assignment. The dictionary maps
        variable names to values. The function cannot change anything in
        `assignment`.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution. The function cannot change
        anything in `gamma`.

    Returns
    -------
    pruned_list : Optional[Pruned]
        In the case that the algorithm detects a conflict, the assignment and
        CSP should remain unchanged and the function should return None.

        Otherwise, the algorithm should return a pruned_list, which is a list
        of (variable, value) pairs that will be pruned out of the domains of
        the variables in the problem. Think of this as the "edits" that are
        required to be done on the variable domains.

    """
    # *** YOUR CODE HERE ***
    output = []
    domain = copy.deepcopy(gamma.current_domains)
    checkList = collections.deque()
    # store all constraint
    for i in gamma.variables:
        for j in gamma.neighbours[i]:
            checkList.append((i, j))
            checkList.append((j, i))

    while len(checkList)>0:
        X_i, X_j = checkList.pop()
        add = False
        for x in domain[X_i].copy():
            correct = False
            for y in domain[X_j].copy():
                if x != y:
                    correct = True
                    break
            if not correct:
                output.append([X_i, x])
                domain[X_i].remove(x)
                add = True    

        if add:
            for X_z in gamma.neighbours[X_i]:
                if X_z != X_j:
                    checkList.append((X_i, X_z))
                    checkList.append((X_z, X_i))
    
    return output


# -------------------------------------------------------------------------------
# A function use to get the correct inference method for the search
# You do not need to touch this.
# -------------------------------------------------------------------------------

def get_inference_function(inference_type: str) -> Callable:
    """Return the function that does the specified inference."""
    if inference_type == "forward":
        return forward_checking
    if inference_type == "arc":
        return arc_consistency

    # If no inference is specified, we simply do nothing.
    def no_inference(var, assignment, csp):
        return []

    return no_inference
