

from core.obj.math.common import _try_math


def f_math_power(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: inter.parse(0, line, args)[2] ** inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )


def f_math_root(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: inter.parse(0, line, args)[2]
        ** (1 / inter.parse(1, line, args)[2]),
        line,
        **kwargs,
    )


def f_math_sqrt(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: inter.parse(0, line, args)[2] ** 0.5,
        line,
        **kwargs,
    )




def f_math_floor(inter, line, args, **kwargs):
    import math
    return _try_math(
        inter,
        lambda: math.floor(inter.parse(0, line, args)[2]),
        line,
        **kwargs,
    )


def f_math_ceil(inter, line, args, **kwargs):
    import math
    return _try_math(
        inter,
        lambda: math.ceil(inter.parse(0, line, args)[2]),
        line,
        **kwargs,
    )


def f_math_round(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: round(inter.parse(0, line, args)[2]),
        line,
        **kwargs,
    )


def f_math_abs(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: abs(inter.parse(0, line, args)[2]),
        line,
        **kwargs,
    )


OBJ_MATH_ADVANCED_DISPATCH = {
    "power": f_math_power,
    "root": f_math_root,
    "sqrt": f_math_sqrt,
    "floor": f_math_floor,
    "ceil": f_math_ceil,
    "round": f_math_round,
    "abs": f_math_abs,
}
