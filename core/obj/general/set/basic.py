

from core.common import aliases
from core.errors import inter_raise_err

def f_obj_set_add(inter, line, args, **kwargs):
    for i in range(len(args)):
        inter.vars[kwargs["vname"]].value.add(inter.parse(i, line, args)[2])
    return inter.vars[kwargs["vname"]].value


def f_obj_set_pop(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.pop()


def f_obj_set_remove(inter, line, args, **kwargs):
    for i in range(len(args)):
        inter.vars[kwargs["vname"]].value.remove(inter.parse(i, line, args)[2])
    return inter.vars[kwargs["vname"]].value


def f_obj_set_list(inter, line, args, **kwargs):
    return list(inter.vars[kwargs["vname"]].value)


def f_obj_set_get(inter, line, args, **kwargs):
    # index to get at
    ind = inter.parse(0, line, args)[2]
    # index must be an int
    inter.type_err([(ind, (int,))], line, kwargs["lines_ran"])
    # get the index
    for i in inter.vars[kwargs["vname"]].value:
        if ind == 0:
            return i
        ind -= 1


OBJ_GENERAL_SET_BASIC_DISPATCH = {
    "pop": f_obj_set_pop,
    "remove": f_obj_set_remove,
    "list": f_obj_set_list,
    "get": f_obj_set_get,
    **aliases(f_obj_set_add, ("add", "put")),
}
