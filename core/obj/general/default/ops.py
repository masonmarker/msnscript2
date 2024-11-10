
from core.common import aliases


def _try_obj_default_math(inter, func, line, **kwargs):
    try:
        return func()
    except:
        inter.raise_operation_err(kwargs["vname"], kwargs["objfunc"], kwargs["lines_ran"])


def _f_obj_default_add(inter, line, args, **kwargs):
    # basic arithmetic, non-destructive
    # takes any amount of arguments
    ret = kwargs["object"]
    for i in range(len(args)):
        ret += inter.parse(i, line, args)[2]
    return ret
def f_obj_default_add(inter, line, args, **kwargs):
    return _try_obj_default_math(
        inter,
        lambda: _f_obj_default_add(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_obj_default_sub(inter, line, args, **kwargs):
    ret = kwargs["object"]
    for i in range(len(args)):
        ret -= inter.parse(i, line, args)[2]
    return ret
def f_obj_default_sub(inter, line, args, **kwargs):
    return _try_obj_default_math(
        inter,
        lambda: _f_obj_default_sub(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_obj_default_mul(inter, line, args, **kwargs):
    ret = kwargs["object"]
    for i in range(len(args)):
        ret *= inter.parse(i, line, args)[2]
    return ret
def f_obj_default_mul(inter, line, args, **kwargs):
    return _try_obj_default_math(
        inter,
        lambda: _f_obj_default_mul(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_obj_default_div(inter, line, args, **kwargs):
    ret = kwargs["object"]
    for i in range(len(args)):
        ret /= inter.parse(i, line, args)[2]
    return ret
def f_obj_default_div(inter, line, args, **kwargs):
    return _try_obj_default_math(
        inter,
        lambda: _f_obj_default_div(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_obj_default_mod(inter, line, args, **kwargs):
    ret = kwargs["object"]
    for i in range(len(args)):
        ret %= inter.parse(i, line, args)[2]
    return ret
def f_obj_default_mod(inter, line, args, **kwargs):
    return _try_obj_default_math(
        inter,
        lambda: _f_obj_default_mod(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_obj_default_pow(inter, line, args, **kwargs):
    ret = kwargs["object"]
    for i in range(len(args)):
        ret **= inter.parse(i, line, args)[2]
    return ret
def f_obj_default_pow(inter, line, args, **kwargs):
    return _try_obj_default_math(
        inter,
        lambda: _f_obj_default_pow(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_obj_default_idiv(inter, line, args, **kwargs):
    ret = kwargs["object"]
    for i in range(len(args)):
        ret //= inter.parse(i, line, args)[2]
    return ret
def f_obj_default_idiv(inter, line, args, **kwargs):
    return _try_obj_default_math(
        inter,
        lambda: _f_obj_default_idiv(inter, line, args, **kwargs),
        line,
        **kwargs,
    )


OBJ_GENERAL_DEFAULT_OPS_DISPATCH = {
    "+": f_obj_default_add,
    "-": f_obj_default_sub,
    "/": f_obj_default_div,
    "%": f_obj_default_mod,
    "**": f_obj_default_pow,
    "//": f_obj_default_idiv,
    **aliases(f_obj_default_mul, ("*", "x")),
}