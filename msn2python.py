# Function for executing .msn2 scripts from a Python environment.
#
# Provides the ability to input values to the script, as well as receive
# an output value from the script.
#
# author : Mason Marker
# date : 6/2/2023
# updated : 10/09/2024

# provides a .msn2 file with input values, and receives the output value
#
# inputs: a list of values to be passed to the script
# returns the specified out value from the script,
# see the .msn2 file in this directory for how input
# values are read and output

import os

# prepare msn2 interpreter
from msnint2 import Interpreter
from core.classes.var import Var

def run(filename, inputs=None):
    # if no inputs are provided, set to empty list
    if not os.path.exists(filename):
        # print a unique not found "error" and quit
        i = Interpreter()
        i.styled_print(
            [
                {"text": "[", "fore": "black"},
                {"text": "MSN2", "fore": "yellow"},
                {"text": "]", "fore": "black"},
                {"text": f" File not found: {filename}", "fore": "red"},
            ]
        )
        exit()
    # opens the file for reading
    f = open(filename, "r", encoding="utf-8")
    script = f.read()

    # create an Interpreter to run the script
    interpreter = Interpreter()

    # reserved keyword for input
    _n = "_msn2_reserved_in__"

    # pass the inputs to the script
    interpreter.vars[_n] = Var(_n, inputs)

    # execute the script
    interpreter.execute(script)

    # prints the prnt() out if specified
    if interpreter.out != "":
        print(interpreter.out)

    # returns the exported value from the script

    _n_out = "_msn2_reserved_out__"

    if _n_out in interpreter.vars:
        return interpreter.vars[_n_out].value
