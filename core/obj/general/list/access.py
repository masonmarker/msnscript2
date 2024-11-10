

from core.common import aliases


def f_obj_list_pop(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.pop()


def f_obj_list_get(inter, line, args, **kwargs):
    # index to get at
    ind = inter.parse(0, line, args)[2]
    # index must be an int
    inter.type_err([(ind, (int,))], line, kwargs["lines_ran"])
    # get the index
    return inter.vars[kwargs["vname"]].value[ind]


def f_obj_list_find(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.find(inter.parse(0, line, args)[2])


def f_obj_list_len(inter, line, args, **kwargs):
    return len(inter.vars[kwargs["vname"]].value)


def f_obj_list_empty(inter, line, args, **kwargs):
    return len(inter.vars[kwargs["vname"]].value) == 0


def f_obj_list_contains(inter, line, args, **kwargs):
    return inter.parse(0, line, args)[2] in inter.vars[kwargs["vname"]].value


def f_obj_list_avg(inter, line, args, **kwargs):
    try:
        return sum(inter.vars[kwargs["vname"]].value) / len(
            inter.vars[kwargs["vname"]].value
        )
    except:
        if not inter.vars[kwargs["vname"]].value:
            inter.raise_empty_array(line)
        else:
            inter.raise_avg(line)


OBJ_GENERAL_LIST_ACCESS_DISPATCH = {
    "pop": f_obj_list_pop,
    "get": f_obj_list_get,
    "find": f_obj_list_find,
    "len": f_obj_list_len,
    "empty": f_obj_list_empty,
    **aliases(f_obj_list_contains, ("contains", "has", "includes")),
    **aliases(f_obj_list_avg, ("avg", "average")),
}
