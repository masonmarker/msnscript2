




from core.classes.var import Var
from core.errors import inter_raise_err

def f_obj_default_copy(inter, line, args, **kwargs):
    if kwargs["objfunc"] == "copy":
        try:
            return kwargs["object"].copy()
        except:
            # no attribute copy
            inter.err(
                "Error copying object.",
                f'Object "{kwargs["obj"]}" does not have attribute "copy".',
                line,
                kwargs["lines_ran"],
            )
def f_obj_default_print(inter, line, args, **kwargs):
    # if no arguments
    if args[0][0] == "":
        print(kwargs["object"])
        return kwargs["object"]
    # if one argument
    elif len(args) == 1:
        # what to print
        to_print = f"{inter.parse(0, line, args)[2]}{kwargs['object']}"
        # print the object
        print(to_print)
        return to_print
    # if two arguments
    elif len(args) == 2:
        # what to print
        to_print = f"{inter.parse(0, line, args)[2]}{kwargs['object']}{inter.parse(1, line, args)[2]}"
        # print the object
        print(to_print)
        # return the printed object
        return to_print
    return kwargs["object"]
def f_obj_default_switch(inter, line, args, **kwargs):
    # other variable name
    other_varname = inter.parse(0, line, args)[2]
    # check variable name
    inter.check_varname(other_varname, line)
    # other_varname must exist in self.vars
    if other_varname not in inter.vars:
        inter.err(
            "Error switching variables.",
            f'Variable name "{other_varname}" does not exist in this context.',
            line,
            kwargs["lines_ran"],
        )
    # switch the variables
    inter.vars[kwargs["vname"]].value, inter.vars[other_varname].value = (
        inter.vars[other_varname].value,
        inter.vars[kwargs["vname"]].value,
    )
    # return the variable
    return inter.vars[kwargs["vname"]].value

def f_obj_default_rename(inter, line, args, **kwargs):
    # get the variable name
    varname = inter.parse(0, line, args)[2]
    # variable name must be a string
    inter.check_varname(varname, line)
    # rename the variable
    inter.vars[varname] = Var(varname, kwargs["object"])
    # delete the old entry
    del inter.vars[kwargs["vname"]]
    # return the variable
    return inter.vars[varname]
def f_obj_default_if(inter, line, args, **kwargs):
    # variable name
    varname = inter.parse(0, line, args)[2]
    # check varname
    inter.check_varname(varname, line)
    new_list = []
    # perform logic
    for el in kwargs["object"]:
        inter.vars[varname] = Var(varname, el)
        if inter.interpret(args[1][0]):
            new_list.append(el)
    return new_list
def f_obj_default_then(inter, line, args, **kwargs):
    # if one argument
    if len(args) == 1 and args[0][0] != "":
        if kwargs["object"]:
            return inter.parse(0, line, args)[2]
        else:
            return
    # if two arguments
    elif len(args) == 2:
        if kwargs["object"]:
            return inter.parse(0, line, args)[2]
        else:
            return inter.parse(1, line, args)[2]
    return inter.raise_ArgumentCountError(
        method="then",
        expected="1 or 2",
        actual=len(args),
        line=line,
        lines_ran=kwargs["lines_ran"],
    )
def f_obj_default_is(inter, line, args, **kwargs):
    return kwargs["object"] is inter.parse(0, line, args)[2]
def f_obj_default_equals(inter, line, args, **kwargs):
    for i in range(len(args)):
        if kwargs["object"] != inter.parse(i, line, args)[2]:
            return False
    return True
def f_obj_default_slice(inter, line, args, **kwargs):
    first = inter.parse(0, line, args)[2]
    second = inter.parse(1, line, args)[2]
    # ensure both arguments are integers or None
    inter.type_err(
        [(first, (int, type(None))), (second, (int, type(None)))],
        line,
        kwargs["lines_ran"],
    )
    return kwargs["object"][first:second]
def f_obj_default_index(inter, line, args, **kwargs):
    return kwargs["object"].index(inter.parse(0, line, args)[2])
def f_obj_default_export(inter, line, args, **kwargs):
    # if an argument is provided
    # export as name
    if args[0][0] != "":
        vname = inter.parse(0, line, args)[2]
        # check vname
        inter.check_varname(vname, line)
        # vname must exist in current context as a variable
        inter.export_err(vname, line)
    else:
        vname = kwargs["vname"]
    inter.parent.vars[vname] = Var(vname, kwargs["object"])
    return kwargs["object"]
def f_obj_default_assert(inter, line, args, **kwargs):
    # asserts that the object is truthful
    if not kwargs["object"]:
        inter.err(
            f"Assertion error in '{line}'",
            "Object is not truthful.",
            line,
            kwargs["lines_ran"],
        )
    return True
# asserts False
def f_obj_default_assert_false(inter, line, args, **kwargs):
    if kwargs["object"]:
        inter.err(
            f"Assertion error in '{line}'",
            "Object is truthful, expected untruthful.",
            line,
            kwargs["lines_ran"],
        )
    return True
def f_obj_default_assert_equals(inter, line, args, **kwargs):
    # takes two arguments, should equal each other
    arg1 = inter.parse(0, line, args)[2]
    # if they are not equal
    if kwargs["object"] != arg1:
        inter.err(
            f"Assertion error in '{line}'",
            f"{kwargs['object']} does not equal {arg1}.",
            line,
            kwargs["lines_ran"],
        )
    return True
def f_obj_default_interpret(inter, line, args, **kwargs):
    return inter.interpret(kwargs["object"])
def f_obj_default_notequals(inter, line, args, **kwargs):
    for i in range(len(args)):
        if kwargs["object"] == inter.parse(i, line, args)[2]:
            return False
    return True
def f_obj_default_and(inter, line, args, **kwargs):
    """Determines the boolean result of kwargs["object"] and all parsed arguments."""
    if inter.arg_count(args) == 0:
        return inter.err(
            "Error in and()",
            "No arguments provided.",
            line,
            kwargs["lines_ran"],
        )
    if not kwargs["object"]:
        return False
    for i in range(len(args)):
        if not inter.parse(i, line, args)[2]:
            return False
    return True
def f_obj_default_or(inter, line, args, **kwargs):
    """Determines the boolean result of kwargs["object"] or any parsed arguments."""
    if inter.arg_count(args) == 0:
        return inter.err(
            "Error in or()",
            "No arguments provided.",
            line,
            kwargs["lines_ran"],
        )
    if kwargs["object"]:
        return True
    for i in range(len(args)):
        if inter.parse(i, line, args)[2]:
            return True
    return False
def f_obj_default_not(inter, line, args, **kwargs):
    """Determines the boolean result of not kwargs["object"]."""
    # throw an error if arguments are provided
    if inter.arg_count(args) != 0:
        return inter.raise_ArgumentCountError(
            method="not",
            expected="0",
            actual=len(args),
            line=line,
            lines_ran=kwargs["lines_ran"],
        )
    return not kwargs["object"]
def f_obj_default_len(inter, line, args, **kwargs):
    return len(kwargs["object"])
def f_obj_default_as(inter, line, args, **kwargs):
    """stores this value as a variable."""
    # takes infinite string arguments
    for i in range(len(args)):
        vname = inter.parse(i, line, args)[2]
        # check vname
        inter.check_varname(vname, line)
        inter.vars[vname] = Var(vname, kwargs["object"])
    return kwargs["object"]


OBJ_GENERAL_DEFAULT_GENERAL_DISPATCH = {
    # all operations
    "assert": f_obj_default_assert,
    "assert:not": f_obj_default_assert_false,
    "assert:equals": f_obj_default_assert_equals,
    "copy": f_obj_default_copy,
    "print": f_obj_default_print,
    "switch": f_obj_default_switch,
    "rename": f_obj_default_rename,
    "if": f_obj_default_if,
    "is": f_obj_default_is,
    "equals": f_obj_default_equals,
    "notequals": f_obj_default_notequals,
    "slice": f_obj_default_slice,
    "index": f_obj_default_index,
    "export": f_obj_default_export,
    "interpret": f_obj_default_interpret,
    "len": f_obj_default_len,
    
    # chaining emphasis
    "then": f_obj_default_then,
    "and": f_obj_default_and,
    "or": f_obj_default_or,
    "not": f_obj_default_not,
    "as": f_obj_default_as
}
