"""In place operations"""


def _try_obj_number_math(inter, func, line, args, **kwargs):
    try:
        return func()
    except:
        inter.raise_operation_err(kwargs["vname"], kwargs["objfunc"], line)


def _f_obj_number_add(inter, line, args, **kwargs):
    for i in range(len(args)):
        inter.vars[kwargs["vname"]].value += inter.parse(i, line, args)[2]
    return inter.vars[kwargs["vname"]].value


def f_obj_number_add(inter, line, args, **kwargs):
    return _try_obj_number_math(
        inter,
        lambda: _f_obj_number_add(inter, line, args, **kwargs),
        line,
        args,
        **kwargs,
    )


def _f_obj_number_sub(inter, line, args, **kwargs):
    for i in range(len(args)):
        inter.vars[kwargs["vname"]].value -= inter.parse(i, line, args)[2]
    return inter.vars[kwargs["vname"]].value


def f_obj_number_sub(inter, line, args, **kwargs):
    return _try_obj_number_math(
        inter,
        lambda: _f_obj_number_sub(inter, line, args, **kwargs),
        line,
        args,
        **kwargs,
    )


def _f_obj_number_mul(inter, line, args, **kwargs):
    for i in range(len(args)):
        inter.vars[kwargs["vname"]].value *= inter.parse(i, line, args)[2]
    return inter.vars[kwargs["vname"]].value


def f_obj_number_mul(inter, line, args, **kwargs):
    return _try_obj_number_math(
        inter,
        lambda: _f_obj_number_mul(inter, line, args, **kwargs),
        line,
        args,
        **kwargs,
    )


def _f_obj_number_div(inter, line, args, **kwargs):
    for i in range(len(args)):
        inter.vars[kwargs["vname"]].value /= inter.parse(i, line, args)[2]
    return inter.vars[kwargs["vname"]].value


def f_obj_number_div(inter, line, args, **kwargs):
    return _try_obj_number_math(
        inter,
        lambda: _f_obj_number_div(inter, line, args, **kwargs),
        line,
        args,
        **kwargs,
    )


def f_obj_number_abs(inter, line, args, **kwargs):
    # can only be performed on numbers
    inter.vars[kwargs["vname"]].value = abs(inter.vars[kwargs["vname"]].value)
    return inter.vars[kwargs["vname"]].value


def f_obj_number_round(inter, line, args, **kwargs):
    # round to the nearest decimal place
    if args[0][0] != "":
        # decimal place to round to
        place = inter.parse(0, line, args)[2]
        # place type must be int
        inter.type_err([(place, (int,))], line, kwargs["lines_ran"])
        inter.vars[kwargs["vname"]].value = round(
            inter.vars[kwargs["vname"]].value, place
        )
    else:
        inter.vars[kwargs["vname"]].value = round(
            inter.vars[kwargs["vname"]].value)
    return inter.vars[kwargs["vname"]].value


def f_obj_number_floor(inter, line, args, **kwargs):
    # using math
    import math

    inter.vars[kwargs["vname"]].value = math.floor(
        inter.vars[kwargs["vname"]].value)
    return inter.vars[kwargs["vname"]].value


def f_obj_number_ceil(inter, line, args, **kwargs):
    # using math
    import math

    inter.vars[kwargs["vname"]].value = math.ceil(
        inter.vars[kwargs["vname"]].value)
    return inter.vars[kwargs["vname"]].value


def f_obj_number_neg(inter, line, args, **kwargs):
    inter.vars[kwargs["vname"]].value = -inter.vars[kwargs["vname"]].value
    return inter.vars[kwargs["vname"]].value


# inplace
OBJ_GENERAL_NUMBER_OPS_IP_DISPATCH = {
    "add": f_obj_number_add,
    "sub": f_obj_number_sub,
    "mul": f_obj_number_mul,
    "div": f_obj_number_div,
    "abs": f_obj_number_abs,
    "round": f_obj_number_round,
    "floor": f_obj_number_floor,
    "ceil": f_obj_number_ceil,
    "neg": f_obj_number_neg,
}
