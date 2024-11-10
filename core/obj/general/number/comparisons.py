


from core.common import aliases

def _try_obj_number_compare(inter, func, line, args, **kwargs):
    try:
        return func()
    except:
        inter.raise_comp(kwargs["objfunc"], kwargs["vname"], line)
def f_obj_number_greater(inter, line, args, **kwargs):
    return _try_obj_number_compare(
        inter,
        lambda: all(
            inter.vars[kwargs["vname"]].value > inter.parse(i, line, args)[2]
            for i in range(len(args))
        ),
        line,
        args,
        **kwargs,
    )
def f_obj_number_less(inter, line, args, **kwargs):
    return _try_obj_number_compare(
        inter,
        lambda: all(
            inter.vars[kwargs["vname"]].value < inter.parse(i, line, args)[2]
            for i in range(len(args))
        ),
        line,
        args,
        **kwargs,
    )
def f_obj_number_greaterequal(inter, line, args, **kwargs):
    return _try_obj_number_compare(
        inter,
        lambda: all(
            inter.vars[kwargs["vname"]].value >= inter.parse(i, line, args)[2]
            for i in range(len(args))
        ),
        line,
        args,
        **kwargs,
    )
def f_obj_number_lessequal(inter, line, args, **kwargs):
    return _try_obj_number_compare(
        inter,
        lambda: all(
            inter.vars[kwargs["vname"]].value <= inter.parse(i, line, args)[2]
            for i in range(len(args))
        ),
        line,
        args,
        **kwargs,
    )


OBJ_GENERAL_NUMBER_COMPARISONS_DISPATCH = {
        # comparisons
    **aliases(f_obj_number_greater, ("greater", "greaterthan", "g")),
    **aliases(f_obj_number_less, ("less", "lessthan", "l")),
    **aliases(f_obj_number_greaterequal, ("greaterequal", "ge")),
    **aliases(f_obj_number_lessequal, ("lessequal", "le")),
}