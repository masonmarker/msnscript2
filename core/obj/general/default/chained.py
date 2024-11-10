"""Chained functions."""


def f_obj_default_noobjfunc(inter, line, args, **kwargs):
    ret = inter.vars[kwargs["vname"]].value
    # for each block
    for arg in args:
        ret = inter.interpret(f"{kwargs['vname']}.{arg[0]}")
    return ret



OBJ_GENERAL_DEFAULT_CHAINED_DISPATCH = {
    "": f_obj_default_noobjfunc,
}