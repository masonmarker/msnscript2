

from core.classes.var import Var


def f_obj_default_string_name(inter, line, args, **kwargs):
    return kwargs["vname"]


def f_obj_default_each(inter, line, args, **kwargs):
    # get the variable name
    varname = inter.parse(0, line, args)[2]
    # check varname
    inter.check_varname(varname, line)
    # try an indexable
    try:
        for i in range(len(kwargs["object"])):
            inter.vars[varname] = Var(varname, kwargs["object"][i])
            inter.interpret(args[1][0])
    except:
        # try a set
        for i in kwargs["object"]:
            inter.vars[varname] = Var(varname, i)
            inter.interpret(args[1][0])
    return kwargs["object"]


def f_obj_default_rfind(inter, line, args, **kwargs):
    return kwargs["object"].rfind(inter.parse(0, line, args)[2])


def f_obj_default_lfind(inter, line, args, **kwargs):
    return kwargs["object"].find(inter.parse(0, line, args)[2])


def f_obj_default_find(inter, line, args, **kwargs):
    return kwargs["object"].find(inter.parse(0, line, args)[2])


def f_obj_default_filter(inter, line, args, **kwargs):
    # get the variable name
    varname = inter.parse(0, line, args)[2]
    # check variable name
    inter.check_varname(varname, line)
    # filtered
    filtered = []
    # filter the iterable
    for el in kwargs["object"]:
        inter.vars[varname] = Var(varname, el)
        if inter.interpret(args[1][0]):
            filtered.append(el)
    # set the variable to the filtered list
    inter.vars[kwargs["vname"]].value = filtered
    # return the filtered list
    return inter.vars[kwargs["vname"]].value


def f_obj_default_func(inter, line, args, **kwargs):
    ret = kwargs["object"]
    # apply the function to the object
    for arg in args:
        ret = inter.interpret(f"{arg[0]}({ret})")
    return ret


def f_obj_default_reverse(inter, line, args, **kwargs):
    # only types that can be reversed:
    # list, tuple, string
    # check types
    inter.type_err(
        [(kwargs["object"], (list, tuple, str))], line, kwargs["lines_ran"]
    )
    inter.vars[kwargs["vname"]].value = kwargs["object"][::-1]
    return inter.vars[kwargs["vname"]].value


def f_obj_default_in(inter, line, args, **kwargs):
    in_var = inter.parse(0, line, args)[2]
    # in_var must be of type iterable
    inter.check_iterable(in_var, line)
    # if object is of type string
    if isinstance(kwargs["object"], str):
        # in_var must be a string also
        inter.type_err([(in_var, (str,))], line, kwargs["lines_ran"])
        return kwargs["object"] in in_var
    else:
        # otherwise, in_var cannot be a string
        if isinstance(in_var, str):
            inter.err(
                "Type error",
                f'Cannot search for type {type(kwargs["object"])} in type {type(in_var)}\nConsider casting variable "{kwargs["vname"]}" to {str}, \nor change in() argument to a different iterable',
                line,
                kwargs["lines_ran"],
            )
    return kwargs["object"] in in_var


OBJ_GENERAL_DEFAULT_STRINGS_DISPATCH = {
    "string_name": f_obj_default_string_name,
    "each": f_obj_default_each,
    "rfind": f_obj_default_rfind,
    "lfind": f_obj_default_lfind,
    "find": f_obj_default_find,
    "filter": f_obj_default_filter,
    "func": f_obj_default_func,
    "reverse": f_obj_default_reverse,
    "in": f_obj_default_in,
}
