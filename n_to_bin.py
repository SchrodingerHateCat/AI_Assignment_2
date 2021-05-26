"""N-ary to binary constraint compiler.

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
import argparse
import os
import sys
from typing import Dict, List, Set, Tuple


def process_command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments and return an object with attributes
    containing the parsed arguments or their default values.

    Returns
    -------
    args : an argparse.Namespace object
        This object will have two attributes:
            - input: a string with the path of the input file specified via
            the command line.
            - output: a string with the path of the file where the binarised
            CSP is to be found.

    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", dest="input", metavar="INPUT",
                        type=str, help="Input file with an n-ary CSP (MANDATORY)")
    parser.add_argument("-o", "--output", dest="output", metavar="OUTPUT",
                        default='binarised.csp',
                        help="File to write the binarised CSP (default: %(default)s)")

    args = parser.parse_args()
    if args.input is None:
        raise SystemExit("Error: No input file was specified.")

    if not os.path.exists(args.input):
        raise SystemExit(
            "Error: Input file '{}' does not exist".format(args.input))

    return args


def main():
    args = process_command_line_arguments()
    input_path = args.input
    output_path = args.output
    variables, constraints = parse_nary_file(input_path)

    # *** YOUR CODE HERE ***
    myDomain = {}

    # read output file
    if args.output is None:
        output_file = sys.stdout
    else:
        try:
            output_file = open(args.output, "w")
        except IOError as e:
            print("Error: could not open output file:", args.output)
            return
    
    # write into Domain variable
    for var in constraints:
        if var[0] not in myDomain:
            myDomain[var[0]] = []
        for val in var[1]:
            myDomain[var[0]].append(val)

    # write variables and domain into CSP file
    for key, value in myDomain.items():
        output_file.write('var <')
        for var in key:
            output_file.write(var)
            if var != key[-1]:
                output_file.write(',')
        output_file.write('> : ')
        for val in myDomain[key]:
            output_file.write('<')
            for j in range(len(val)):
                output_file.write(val[j])
                if j != len(val)-1:
                    output_file.write(',')
            output_file.write('> ')
        output_file.write('\n')

    # domain size must greater than 1
    if len(myDomain) >= 2:
        for res in combination(len(myDomain), 2):           # from m choose n 
            # create constraints key
            # for example:
            # <x,y> <y,z>
            constraintsKey = []
            constraintsKey.append(constraints[res[0]][0])
            constraintsKey.append(constraints[res[1]][0])
            # make checkList
            # which represent the index need to check
            # for example:
            # con <x,y><y,z> need to check 2nd of <x,y> == 1st of <y,z>
            # so the checkList will be [1,0]
            checkList = []
            for x in range(len(constraints[res[0]][0])):
                for y in range(len(constraints[res[1]][0])):
                    if constraints[res[0]][0][x] == constraints[res[1]][0][y]:
                        checkList.append([x,y])
            # same as Constraints key
            # here we add values of constraints
            # for example
            # <5,2><2,7> for <x,y><y,z>
            constraintsVal = []
            for i in constraints[res[0]][1]:
                for j in constraints[res[1]][1]:
                    correct = True
                    for z in checkList:
                        if i[z[0]] != j[z[1]]:
                            correct = False
                    if correct:
                        constraintsVal.append([i,j])

            if len(constraintsVal) <= 0:
                raise ValueError('Unsatisfiable constraints')


            # write constraints into CSP file after checking constraints is empty or not
            output_file.write('con ')
            for var in constraintsKey:
                output_file.write('<')
                for var_i in var:
                    output_file.write(var_i)
                    if var_i != var[-1]:
                        output_file.write(',')
                output_file.write('> ')
           
            for val in constraintsVal:
                output_file.write(': ')
                for val_j in val:
                    output_file.write('<')
                    for val_j_j in range(len(val_j)):
                        output_file.write(val_j[val_j_j])
                        if val_j_j != len(val_j)-1:
                            output_file.write(',')
                    output_file.write('> ')
            output_file.write('\n')
    else:
        raise ValueError('Unsatisfiable constraints')


# doing combination C_n_m
def combination(n,c,com=1,limit=0,per=[]):
    for pos in range(limit,n):
        t = per + [pos]
        if len(set(t)) == len(t):
            if len(t) == c:
                    yield [pos,]
            else:
                    for result in combination(n,c,com,com*pos, per + [pos,]):
                            yield [pos,] + result
# -----------------------------------------------------------------------------
# You might like to use the helper functions below. Feel free to modify these
# functions to suit your needs.
# -----------------------------------------------------------------------------


def parse_nary_file(file_name: str):
    """Parse an n-ary CSP file.

    Parameters
    ----------
    file_name : str
        The path to the n-ary CSP file.

    Returns
    -------
    variables : Dict[str, Set[str]]
        A dictionary mapping variable names to their domains. Each domain is
        represented by a set of values.

    constraints : List[Tuple[Tuple[str, ...], List[Tuple[str, ...]]]]
        A list of constraints. Each constraint is a tuple with two elements:
            1) The first element is the tuple of the variables involved in the
               constraint, e.g. ('x', 'y', 'z').

            2) The second element is the list of values those variables are
               allowed to take, e.g. [('0', '0', '0'), ('0', '1', '1')].

    """
    variables: Dict[str, Set[str]] = {}
    constraints: List[Tuple[Tuple[str, ...], List[Tuple[str, ...]]]] = []

    with open(file_name, "r") as file:
        for line in file:
            if line.startswith('var'):
                var_names, domain = line[3:].split(':')
                domain_set = set(domain.split())
                for v in var_names.split():
                    variables[v] = domain_set

            elif line.startswith('con'):
                content = line[3:].split(':')
                vs = tuple(content[0].split())
                values = [tuple(v.split()) for v in content[1:]]
                constraints.append((vs, values))

    return variables, constraints


if __name__ == '__main__':
    main()
