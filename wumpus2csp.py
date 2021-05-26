"""Wumpus World.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: COMP-3620 team
Date: 2021

Student Details
---------------
Student Name:
Student Number:
Date:
"""
import argparse
import os
import sys


def process_command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments and return an object with attributes
    containing the parsed arguments or their default values.
    """
    import json

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", dest="input", metavar="INPUT",
                        type=str, help="Input file with the Wumpus World parameters and observations (MANDATORY)")
    parser.add_argument("-a", "--action", dest="action", metavar="ACTION",
                        type=str, choices=["north", "south", "east", "west"],
                        help="Action to be tested for safety (MANDATORY)")
    parser.add_argument("-o", "--output", dest="output", metavar="OUTPUT", default='wumpus_outputs',
                        help="Output folder (default: %(default)s)")

    args = parser.parse_args()
    if args.action is None:
        raise SystemExit("Error: No action was specified.")

    if args.input is None:
        raise SystemExit("Error: No input file was specified.")

    if not os.path.exists(args.input):
        raise SystemExit(
            "Error: Input file '{}' does not exist".format(args.input))

    try:
        with open(args.input) as instream:
            args.domain_and_observations = json.load(instream)
    except IOError:
        raise SystemExit("Error: could not open file {}".format(args.input))

    return args


def main():
    # Processes the arguments passed through the command line
    args = process_command_line_arguments()

    # The name of the action to test
    action = args.action

    # The path of the directory that will contain the generated CSP files
    output_path = args.output

    # The description of the Wumpus World features and sequence of observations
    # resulting from the agent actions.
    dao = args.domain_and_observations
    n_rows = dao["rows"]
    n_columns = dao["columns"]
    n_wumpuses = dao["wumpuses"]
    n_pits = dao["pits"]
    observations = dao["observations"]

    # YOUR CODE HERE
    if args.output is None:
        output_file = sys.stdout
    else:
        try:
            output_file = open(args.output, "w")
        except IOError as e:
            print("Error: could not open output file:", args.output)
            return
    
    variables = []

    createVariableDomain(n_rows,n_columns,output_file,variables)
    createBConstraints(2, 2,n_rows,n_columns, output_file)
    createSConstraints(2, 1,n_rows,n_columns, output_file)


def createVariableDomain(row, column, file, variables):
    for i in range(row,0,-1):
        file.write('var ')
        for j in range(1,column+1):
            file.write('P_' + str(j)+str(i)+' ')
            variables.append('P_' + str(j)+str(i)+' ')
        #file.write(': P W B S O PB PS WB WS BA SA OA BS BSA PBS WBS')
        file.write(': 0 1')
        file.write('\n')
    
    for i in range(row,0,-1):
        file.write('var ')
        for j in range(1,column+1):
            file.write('W_' + str(j)+str(i)+' ')
            variables.append('W_' + str(j)+str(i)+' ')
        #file.write(': P W B S O PB PS WB WS BA SA OA BS BSA PBS WBS')
        file.write(': 0 1')
        file.write('\n')
    file.write('\n')


def createPConstraints(x, y, rows, columns,file):
    file.write('con '+str(x)+str(y) +' : B : PB : WB : PBS : WBS : BA : BS : BSA\n')
    if x + 1 <= columns:
        file.write('con '+str(x+1)+str(y) +' : P : PB : PS : PBS\n')
    if x - 1 > 0:
        file.write('con '+str(x-1)+str(y) +' : P : PB : PS : PBS\n')
    if y + 1 <= rows:
        file.write('con '+str(x)+str(y+1) +' : P : PB : PS : PBS\n')
    if y -1 > 0:
        file.write('con '+str(x)+str(y-1) +' : P : PB : PS : PBS\n')
    file.write('\n')

def createSConstraints(x, y, rows, columns,file):
    file.write('con '+str(x)+str(y) +' : S : PS : WS : PBS : WBS : SA : BS : BSA\n')
    if x + 1 <= columns:
        file.write('con '+str(x+1)+str(y) +' : W : WB : WS : WBS\n')
    if x - 1 > 0:
        file.write('con '+str(x-1)+str(y) +' : W : WB : WS : WBS\n')
    if y + 1 <= rows:
        file.write('con '+str(x)+str(y+1) +' : W : WB : WS : WBS\n')
    if y -1 > 0:
        file.write('con '+str(x)+str(y-1) +' : W : WB : WS : WBS\n')
    file.write('\n')
def createCurrentPositionConstraints(x, y, file):
    file.write('con '+str(x)+str(y) +' : OA : BA : SA : BSA')


def createNothingHappenedConstraints(x, y, file):
    file.write('con '+str(x)+str(y) +' : O : OA')
    if x + 1 <= n_columns:
        file.write('con '+str(x+1)+str(y) +' : B : S : O : BA : SA : OA : BS : BSA')
    if x - 1 > 0:
        file.write('con '+str(x-1)+str(y) +' : B : S : O : BA : SA : OA : BS : BSA')
    if y + 1 <= n_rows:
        file.write('con '+str(x)+str(y+1) +' : B : S : O : BA : SA : OA : BS : BSA')
    if y -1 > 0:
        file.write('con '+str(x)+str(y-1) +' : B : S : O : BA : SA : OA : BS : BSA')

if __name__ == '__main__':
    main()
