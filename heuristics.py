"""Heuristics for variable selection and value ordering.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: COMP-3620 team
Date:    2021

Student Details
---------------
Student Name:
Student Number:
Date:

This is where you need to write your heuristics for variable selection and
value ordering.
"""
from typing import Callable, Dict, List, Optional
import sys
from csp import CSP
import operator
import copy
import functools
Assignment = Dict[str, str]


# -----------------------------------------------------------------------------
# Variable Selection Heuristics
# -----------------------------------------------------------------------------


def next_variable_lex(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Select the next variable by lexicographic order.

    Select the next variable from the remaining variables according to
    lexicographic order. We have implemented this one for you.

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
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # gamma.variables is a list of variable names (as strings). See line 43 in
    # csp.py. We consider them in the order they are added in.
    for var in sorted(gamma.variables):
        if var not in assignment:
            return var
    return None


def next_variable_md(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement the most constraining variable (MD) heuristic.

    Choose the variable that that is involved in as many constraints as
    possible. See Lecture 11 for the precise definition. Break ties by
    lexicographic order.

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
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    #raise NotImplementedError("Error: MD heuristic not implemented yet!")
    maxVar = None
    maxNum = -1

    for var in sorted(gamma.variables):
        if var not in assignment:
            neighbour = gamma.neighbours[var]
            # number is the sum of variable's neighbour which not in assignment
            number = sum([1 for val in neighbour if val not in assignment])
            # check if the number is greater than our existing number
            # we want to choose the largest one
            if number > maxNum:
                maxVar = var
                maxNum = number
    return maxVar

def next_variable_mrv(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement the most constrained variable heuristic (MRV).

    Choose the variable with the smallest consistent domain. See Lecture 11 for
    the precise definition. Break ties by lexicographic order.

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
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    #raise NotImplementedError("Error: MRV heuristic not implemented yet!")
    minVar = None
    minNum = sys.maxsize
    
    domain = copy.deepcopy(gamma.current_domains)
    # domain number is the variable to numbers of domains
    domain_number = {key: len(value) for key, value in domain.items()}
    for var in sorted(gamma.variables):
        # here we choose the smallest size of domain
        if var not in assignment and domain_number[var] < minNum:
            minVar = var
            minNum = domain_number[var]

    return minVar

def next_variable_md_mrv(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement MD heuristic, breaking ties with MRV.

    Choose the variable that is involved in as many constraints as possible. If
    there is a tie, choose the variable with the smallest consistent domain.
    See Lecture 11 for the precise definition.

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
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # *** YOUR CODE HERE ***
    #raise NotImplementedError("Error: MD/MRV heuristic not implemented yet!")
    maxVar = None
    maxNum = -1
    # implement the MD first
    for var in sorted(gamma.variables):
        if var not in assignment:
            neighbour = gamma.neighbours[var]
            number = sum([1 for val in neighbour if val not in assignment])
            if number > maxNum:
                maxVar = var
                maxNum = number
            # if they have same number:
            # then implement the MRV
            elif number == maxNum:
                if len(gamma.domains[var]) < len(gamma.domains[maxVar]):
                    maxVar = var
                    maxNum = number
    return maxVar


def next_variable_mrv_md(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement MRV heuristic, breaking ties with MD.

    Choose the variable with the smallest consistent domain. If there is a tie,
    choose the variable that is involved in as many constraints as
    possible. See Lecture 11 for the precise definition.

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
    # *** YOUR CODE HERE ***
    #raise NotImplementedError("Error: MRV/MD heuristic not implemented yet!")
    minVar = None
    minNum = float('inf')

    for var in sorted(gamma.variables):
        if var not in assignment:
            if len(gamma.current_domains[var]) < minNum:
                minVar = var
                minNum = len(gamma.current_domains[var])
            elif len(gamma.current_domains[var]) == minNum:
                neighbour_origin = gamma.neighbours[minVar]
                neighbour_next = gamma.neighbours[var]
                origin_num = sum([1 for val in neighbour_origin if val not in assignment])
                next_num = sum([1 for val in neighbour_next if val not in assignment])
                if next_num > origin_num:
                    minVar = var
                    minNum = len(gamma.current_domains[var])

    return minVar


# -----------------------------------------------------------------------------
# Value Ordering Heuristics
# -----------------------------------------------------------------------------


def value_ordering_lex(var: str, assignment: Assignment, gamma: CSP) -> List[str]:
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
    return sorted(gamma.current_domains[var])


def value_ordering_lcvf(var: str, assignment: Assignment, gamma: CSP) -> List[str]:
    """Order the values based on the Least Constraining Value heuristic.

    This heuristic returns values in order of how constraining they are. It
    prefers the value that rules out the fewest choices for the neighbouring
    variables in the constraint graph. In other words,  it prefers values which
    remove the fewest elements from the current domains of their neighbouring
    variables.

    See Lecture 11 for the precise definition. You might find the attribute
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
        All the values in  the current domain of the variable, sorted according
        to this heuristic.

    """
    # *** YOUR CODE HERE ***
    #raise NotImplementedError("Error: LCVF heuristic not implemented yet!")

    domain = sorted(copy.deepcopy(gamma.current_domains[var]))
    solution = []
    while len(domain) > 0:
        minVal = None
        minNum = float('inf')
        for val in domain:
            conflicts = gamma.count_conflicts(var, val)
            if conflicts < minNum:
                minNum = conflicts
                minVal = val
        solution.append(minVal)
        domain.remove(minVal)
    
    return solution

# -------------------------------------------------------------------------------
# Functions used by the system to select from the above heuristics for the search
# You do not need to look any further.
# -------------------------------------------------------------------------------

def get_variable_selection_function(variable_heuristic: str) -> Callable:
    """Return the appropriate variable selection function."""
    if variable_heuristic == "lex":
        return next_variable_lex
    if variable_heuristic == "md":
        return next_variable_md
    if variable_heuristic == "mrv":
        return next_variable_mrv
    if variable_heuristic == "md-mrv":
        return next_variable_md_mrv
    if variable_heuristic == "mrv-md":
        return next_variable_mrv_md

    raise ValueError(f"Error: the variable selection heuristic "
                     f"'{variable_heuristic}' is not supported")


def get_value_ordering_function(value_heuristic: str) -> Callable:
    """Return the appropriate value ordering function."""
    if value_heuristic == "lex":
        return value_ordering_lex
    if value_heuristic == "lcvf":
        return value_ordering_lcvf

    raise ValueError(f"Error: the value selection heuristic "
                     f"'{value_heuristic}' is not supported")
