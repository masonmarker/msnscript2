"""Class to determine if the interpreter should continue interpreting.
This is a special class to mark a function as without a return.

This is not for in-lang use, but for the interpreter to use.
"""


class Continue:
    def __init__(self):
        pass