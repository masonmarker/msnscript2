# MSN2 instruction
#
# author : Mason Marker
# date : 12/16/2023
# version : 2.0.400

# imports
from core.using_js.js import convert_to_js

# standard MSN2 instruction


class Instruction():
    def __init__(self, line, func, obj, objfunc, args, inst_tree, interpreter):
        self.line = line
        self.func = func
        self.obj = obj
        self.objfunc = objfunc
        self.args = args
        self.tree = inst_tree
        self.interpreter = interpreter
        self.in_html = False
    # parses an argument

    def parse(self, i):
        return self.interpreter.parse(i, self.line, self.args)[2]
    # interprets this instruction line

    def interpret(self):
        return self.interpreter.interpret(self.line)
    # determines if this instruction has arguments or not
    def has_args(self):
        return self.args[0][0] != ''
    
    # coverts this instruction to JavaScript

    def convert_to_js(self, lock, lines_ran):
        return convert_to_js(self, lock, lines_ran)
    # converts and runs JavaScript

    def convert_and_run_js(self, lock, lines_ran):
        js = self.convert_to_js(lock, lines_ran)
        return self.interpreter.interpret(f"JS({js})")
    # checks for a type error

    def type_err(self, types, lines_ran):
        self.interpreter.type_err(types, self.line, lines_ran)
    # str

    def __str__(self):
        from msnint2 import Interpreter
        return Interpreter.bordered(f"Interpreter:\nline: {self.line}\nfunc: {self.func}\nobj: {self.obj}\nobjfunc: {self.objfunc}\nargs: {self.args}\ninterpreter: {self.interpreter}")
