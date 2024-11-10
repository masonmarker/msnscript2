

from core.common import aliases
from core.classes.var import Var


def f_obj_list_push(inter, line, args, **kwargs):
    for i in range(len(args)):
        inter.vars[kwargs["vname"]].value.append(inter.parse(i, line, args)[2])
    return inter.vars[kwargs["vname"]].value


def f_obj_list_set(inter, line, args, **kwargs):
    ind = inter.parse(0, line, args)[2]
    # index must be an int
    inter.type_err([(ind, (int,))], line, kwargs["lines_ran"])
    inter.vars[kwargs["vname"]].value[ind] = inter.parse(1, line, args)[2]
    return inter.vars[kwargs["vname"]].value


def f_obj_list_insert(inter, line, args, **kwargs):
    for i in range(len(args)):
        ind = inter.parse(i, line, args)[2]
        # index must be an int
        inter.type_err([(ind, (int,))], line, kwargs["lines_ran"])
        val = inter.parse(i, line, args)[2]
        inter.vars[kwargs["vname"]].value.insert(ind, val)
    return inter.vars[kwargs["vname"]].value


def f_obj_list_removen(inter, line, args, **kwargs):
    count = inter.parse(0, line, args)[2]
    # count must be an int
    inter.type_err([(count, (int,))], line, kwargs["lines_ran"])
    for i in range(1, len(args)):
        for j in range(count):
            val = inter.parse(i, line, args)[2]
            try:
                del inter.vars[kwargs["vname"]].value[
                    (
                        _v := inter.vars[kwargs["vname"]].value.index(val)
                    )
                ]
            except ValueError:
                inter.raise_value(val, line)
    return inter.vars[kwargs["vname"]].value


def f_obj_list_remove(inter, line, args, **kwargs):
    for i in range(len(args)):
        while inter.parse(i, line, args)[2] in inter.vars[kwargs["vname"]].value:
            try:
                del inter.vars[kwargs["vname"]].value[
                    (
                        _v := inter.vars[kwargs["vname"]].value.index(
                            inter.parse(i, line, args)[2]
                        )
                    )
                ]
            except ValueError:
                inter.raise_value(_v, line)
    return inter.vars[kwargs["vname"]].value


def f_obj_list_sorted(inter, line, args, **kwargs):
    return sorted(inter.vars[kwargs["vname"]].value)


def f_obj_list_sort(inter, line, args, **kwargs):
    inter.vars[kwargs["vname"]].value.sort()
    return inter.vars[kwargs["vname"]].value


def f_obj_list_shuffle(inter, line, args, **kwargs):
    import random

    random.shuffle(inter.vars[kwargs["vname"]].value)
    return inter.vars[kwargs["vname"]].value


def f_obj_list_map(inter, line, args, **kwargs):
    # get the variable name
    varname = inter.parse(0, line, args)[2]
    # check varname
    inter.check_varname(varname, line)
    for i in range(len(inter.vars[kwargs["vname"]].value)):
        inter.vars[varname] = Var(
            varname, inter.vars[kwargs["vname"]].value[i])
        inter.vars[kwargs["vname"]].value[i] = inter.interpret(args[1][0])
    del inter.vars[varname]
    return inter.vars[kwargs["vname"]].value


def f_obj_list_join(inter, line, args, **kwargs):
    delimiter = inter.parse(0, line, args)[2]
    # delimiter must be a string
    inter.type_err([(delimiter, (str,))], line, kwargs["lines_ran"])
    return delimiter.join(map(str, inter.vars[kwargs["vname"]].value))


def f_obj_list_toset(inter, line, args, **kwargs):
    return set(inter.vars[kwargs["vname"]].value)


OBJ_GENERAL_LIST_MODIFY_DISPATCH = {
    "set": f_obj_list_set,
    "insert": f_obj_list_insert,
    "removen": f_obj_list_removen,
    "remove": f_obj_list_remove,
    "map": f_obj_list_map,
    "toset": f_obj_list_toset,
    "shuffle": f_obj_list_shuffle,
    "sorted": f_obj_list_sorted,
    "sort": f_obj_list_sort,
    **aliases(f_obj_list_join, ("join", "delimit")),
    **aliases(f_obj_list_push, ("push", "append", "add")),
}
