"""Variable based functions."""

from core.classes.var import Var



def f_var(inter, line: str, args, **kwargs):
    # extract varname
    varname = inter.parse(0, line, args)[2]
    # must be varname
    inter.check_varname(varname, line)
    # extract value
    value = inter.parse(1, line, args)[2]
    unsafe = False
    if len(args) == 3:
        # get the unsafe argument
        unsafe = inter.parse(2, line, args)[2]
        # unsafe must be a bool
        inter.type_err([(unsafe, (bool,))], line, kwargs["lines_ran"])
    # get optional UNSAFE argument to force setting
    # add / set variable
    inter.vars[varname] = Var(varname, value, force_allow_name=unsafe)
    return value

def f_exists(inter, line: str, args, **kwargs):
    arg = inter.parse(0, line, args)[2]
    # arg must be str
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    return arg in inter.vars

def f_destroy(inter, line, args, **kwargs):
    for i in range(len(args)):
        varname = inter.parse(i, line, args)[2]
        # varname must be varname
        inter.check_varname(varname, line)
        # must be a varname
        # deletes all variables or methods that start with '__'
        if varname == "__":
            for key in list(inter.vars):
                if key.startswith("__"):
                    del inter.vars[key]
            return True
        if varname in inter.vars:
            del inter.vars[varname]
        elif varname in inter.methods:
            del inter.methods[varname]
    return True

def f_add(inter, line: str, args, **kwargs):
    first = inter.parse(0, line, args)[2]
    second = inter.parse(1, line, args)[2]
    # first must be a varname
    inter.check_varname(first, line)
    # case array
    if isinstance(inter.vars[first].value, list):
        inter.vars[first].value.append(second)
    # case string or number
    else:
        inter.vars[first].value += second
    return inter.vars[first].value

def f_sub(inter, line, args, **kwargs):
    vn = inter.parse(0, line, args)[2]
    # vn must be a variable name
    inter.check_varname(vn, line)
    # gets the substring
    other = inter.parse(1, line, args)[2]
    inter.vars[vn].value -= other
    return inter.vars[vn].value
def f_mul(inter, line, args, **kwargs):
    vn = inter.parse(0, line, args)[2]
    # vn must be a variable name
    inter.check_varname(vn, line)
    # gets the substring
    other = inter.parse(1, line, args)[2]
    inter.vars[vn].value *= other
    return inter.vars[vn].value
def f_div(inter, line, args, **kwargs):
    vn = inter.parse(0, line, args)[2]
    # vn must be a variable name
    inter.check_varname(vn, line)
    # gets the substring
    other = inter.parse(1, line, args)[2]
    inter.vars[vn].value /= other
    return inter.vars[vn].value
def f_append(inter, line, args, **kwargs):
    vn = inter.parse(0, line, args)[2]
    # vn must be a variable name
    inter.check_varname(vn, line)
    other = inter.parse(1, line, args)[2]
    # appends to the array
    inter.vars[vn].value.append(other)
    return inter.vars[vn].value
def f_mod(inter, line: str, args, **kwargs):
    arg1 = inter.parse(0, line, args)[2]
    arg2 = inter.parse(1, line, args)[2]
    _allowed = (int, float, complex, str)
    # verify both arguments are either int or float or complex or str
    inter.type_err(
        [
            (arg1, _allowed),
            (arg2, _allowed),
        ],
        line,
        kwargs["lines_ran"],
    )
    # both types must be int or float
    return arg1 % arg2
def f_val(inter, line, args, **kwargs):
    varname = inter.parse(0, line, args)[2]
    # varname must be a varname
    inter.check_varname(varname, line)
    try:
        return inter.vars[varname].value
    except:
        return inter.vars[varname]
def f_del(inter, line, args, **kwargs):
    for i in range(len(args)):
        first = inter.parse(i, line, args)[2]
        # first must be a varname
        inter.check_varname(first, line)
        del inter.vars[first]
    return True

VARS_DISPATCH = {
    "var": f_var,
    "exists": f_exists,
    "destroy": f_destroy,
    "add": f_add,
    "sub": f_sub,
    "mul": f_mul,
    "div": f_div,
    "append": f_append,
    "mod": f_mod,
    "val": f_val,
    "del": f_del,
}