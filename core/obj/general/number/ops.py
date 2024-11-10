"""General operations. (not in-place)"""

from core.common import aliases


def f_obj_number_inc(inter, line, args, **kwargs):
    inter.vars[kwargs["vname"]].value += 1
    return inter.vars[kwargs["vname"]].value
def f_obj_number_dec(inter, line, args, **kwargs):
    inter.vars[kwargs["vname"]].value -= 1
    return inter.vars[kwargs["vname"]].value
def f_obj_number_even(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value % 2 == 0
def f_obj_number_odd(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value % 2 != 0


# operations (not in place)
OBJ_GENERAL_NUMBER_OPS_DISPATCH = {
    "even": f_obj_number_even,
    "odd": f_obj_number_odd,                
    **aliases(f_obj_number_inc, ("++", "inc")),
    **aliases(f_obj_number_dec, ("--", "dec")),
}