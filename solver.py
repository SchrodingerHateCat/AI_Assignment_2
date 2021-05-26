# COMP3620/6320 Artificial Intelligence
# The Australian National University
# Authors: COMP-3620 team
# Date:    2021

""" This is the base file of the CSP solver.

    It can solve CSPs with binary and unary constraints as well as
    alldiff and allsame constraints. These latter constraints are decomposed
    into binary constraints by the system.

    It has a special output mode to nicely format the solutions to Sudoku
    problems with a given format.

    See problem_syntax.txt for a description of the file format.

    Run the solver with the -h flag for usage information.

    It should not be necessary to look at the code in this file.

    ********** Do not modify any code in this file **********
"""

import argparse
import os
import random
import sys

from csp import CSP
from heuristics import (get_value_ordering_function,
                        get_variable_selection_function)
from inference import get_inference_function

try:
    val = int(os.environ['PYTHONHASHSEED'])
except Exception as e:
    val = None

if val != 1:
    # We simply set the environment variable and re-call ourselves.
    import subprocess

    os.environ["PYTHONHASHSEED"] = '1'

    with open('python.version', 'w') as output_redirect:
        subprocess.run(["python", "-V"], stdout=output_redirect,
                       stderr=subprocess.STDOUT)
    version = None
    with open('python.version') as output_redirect:
        version = output_redirect.read()
        version = tuple([tok for tok in version.split(' ')[1].split('.')])
    major = int(version[0])
    if major == 2:
        print("'python' refers to Python 2.x, trying to invoke Python 3.x with command 'python3'")
        output = subprocess.run(["python3", "-OO"] + sys.argv)
    else:
        subprocess.run(["python", "-OO"] + sys.argv)
    sys.exit(1)


def parse_cmd_line_args() -> argparse.Namespace:
    """ Parse the command line arguments and return an object with attributes
        containing the parsed arguments or their default values.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_name", metavar="INPUT",
                        help="The path to the input CSP file.")
    parser.add_argument("-o", "--output", dest="output_file_name", metavar="OUTPUT",
                        help="If given, write the grounded CSP to this file (and don't solve it).")
    parser.add_argument("-s", "--solution", dest="solution_file_name", metavar="SOLUTION",
                        help="If given, write the satisfying assignment to this file.")
    parser.add_argument("-S", "--search", dest="search_algorithm", metavar="SEARCH",
                        choices=["backtracking", "local"], default="backtracking",
                        help="Choose a search algorithm from [%(choices)s] (default: %(default)s)")
    parser.add_argument("-R", "--seed", dest="rng_seed", metavar="RNG", type=int, default=8193,
                        help="Select a seed for the random number generator (default: %(default)s)")
    parser.add_argument("-v", "--var_heuristic", dest="variable_heuristic",
                        choices=["lex", "md", "mrv", "md-mrv", "mrv-md"], default="lex",
                        metavar="VAR", help="Choose a variable selection heuristic from " +
                        "[%(choices)s] (default: %(default)s)")
    parser.add_argument("-l", "--val_heuristic", dest="value_heuristic",
                        choices=["lex", "lcvf"], default="lex",  metavar="VAL",
                        help="Choose a value selection heuristic from " +
                        "[%(choices)s] (default: %(default)s)")
    parser.add_argument("-p", "--preprocessing", dest="preprocessing",
                        choices=["arc"], default=None,  metavar="PRE",
                        help="Choose an inference function to use as a preprocessing step before search:" +
                        "[%(choices)s]. If not given, no preprocessing is used.")
    parser.add_argument("-i", "--inference", dest="search_inference",
                        choices=["forward", "arc"], default=None,  metavar="INF",
                        help="Choose an inference function that runs during search: " +
                        "[%(choices)s]. If not given, no inference is used.")
    parser.add_argument("-t", "--max_steps", dest="max_steps", type=int, default=10000,
                        metavar="MAX_STEPS", help="The maximum number of steps used for Local Search (default: %(default)s)")
    parser.add_argument("-k", "--sudoku", dest="sudoku_output",
                        action="store_true", default=False,
                        help="Interpret the solution as Sudoku output and display it in the terminal.")

    args = parser.parse_args()

    """
    print ("Command line options:")
    print ("    Input file:         ", args.input_file_name)
    print ("    Output file:        ", args.output_file_name)
    print ("    Solution file:      ", args.solution_file_name)
    print ("    Variable heuristic: ", args.variable_heuristic)
    print ("    Value heuristic:    ", args.value_heuristic)
    print ("    Search:             ", args.search-algorithm)
    print ("    Preprocessing:      ", args.preprocessing)
    print ("    Search Inference:   ", args.search_inference)
    print ("    Sudoku output:      ", args.sudoku_output)
    """

    return args


def main():
    """ Parse the command line arguments. Make the CSP object. Do preprocessing
        if requested. Then call the search object.
        () -> None
    """
    args = parse_cmd_line_args()

    print("Random Number Generator Seed: {}".format(args.rng_seed))
    random.seed(args.rng_seed)

    # Get the appropriate functions to be used by the search
    variable_selection_function = get_variable_selection_function(
        args.variable_heuristic)
    value_ordering_function = get_value_ordering_function(args.value_heuristic)
    inference_pre_function = get_inference_function(args.preprocessing)
    inference_search_function = get_inference_function(args.search_inference)

    print("Parsing CSP file:", args.input_file_name)
    csp = CSP()
    if not csp.parse_csp_file(args.input_file_name):
        return
    print("Success.")

    # We can't make any initial assignment. Suppose we have:
    #   var a : 1
    #   var b : 1
    #   neq a b
    #
    # Under this condition, there should be no solution for this problem since
    # a != b and they have the only same value in their domains. However the
    # solver doesn't even bother to check for the constraint and return a
    # solution too soon. To fix this, we prevent the solver from assigning
    # values to variables with unary constraints during preprocessing, i.e.
    # uncomment the code below
    #
    # initial_assignment = dict([(var, csp.domains[var][0])
    #                            for var in csp.variables if len(csp.domains[var]) == 1])
    initial_assignment = {}

    # Apply preprocessing if requested
    if inference_pre_function is not None:
        print("Preprocessing...")
        result = inference_pre_function(None, initial_assignment, csp)

        if result is None:
            print("Error: inconsistency detected in preprocessing.")
            return
        csp.notify_of_inference(None, initial_assignment, result)
        print("Preprocessing pruned", len(result), "values.")

    if args.output_file_name is not None:
        print("Writing grounded CSP to:", args.output_file_name)
        try:
            with open(args.output_file_name, "w") as output_file:
                csp.write(output_file)
        except IOError as e:
            print("Error: cannot open output file:", args.output_file_name)
        return

    search = None
    if args.search_algorithm == "backtracking":
        import backtracking_search
        print("Search algorithm: Backtracking")
        assignment, explored, search_time = backtracking_search.search(csp, initial_assignment,
                                                                       variable_selection_function, value_ordering_function, inference_search_function)

    elif args.search_algorithm == "local":
        import local_search
        print("Search algorithm: Local Search")
        assignment, explored, search_time = local_search.search(csp, initial_assignment,
                                                                variable_selection_function, value_ordering_function, args.max_steps)
    else:
        raise SystemExit(
            "[Fatal]: Search algorithm {} is not supported!".format(args.search_algorithm))

    if args.solution_file_name is None:
        solution_file = sys.stdout
    else:
        try:
            solution_file = open(args.solution_file_name, "w")
        except IOError as e:
            print("Error: could not open output file:", args.solution_file_name)
            return

    # Display the result
    if assignment is None:
        print("There is no solution!")
        solution_file.write("UNSAT\n")
        solution_file.write("Explored: " + str(explored) + "\n")
        solution_file.write("Time: " + str(search_time) + "\n")
    else:
        print("Solution found.")
        if args.sudoku_output:
            for y in range(1, 10):
                for x in range(1, 10):
                    solution_file.write(assignment[str(x)+str(y)] + " ")
                    if x % 3 == 0 and x < 9:
                        solution_file.write("| ")
                solution_file.write("\n")
                if y % 3 == 0 and y < 9:
                    solution_file.write("---------------------\n")
        else:
            solution_file.write("SAT\n")
            solution_file.write("Explored: " + str(explored) + "\n")
            solution_file.write("Time: " + str(search_time) + "\n")
            solution_file.write("Solution: " + " ".join([var+"="+val
                                                         for var, val in assignment.items()]) + "\n")


if __name__ == "__main__":
    main()
