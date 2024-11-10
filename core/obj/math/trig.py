

from core.obj.math.common import _try_math


def f_math_sin(inter, line, args, **kwargs):
    import math
    return _try_math(
        inter,
        lambda: math.sin(inter.parse(0, line, args)[2]),
        line,
        **kwargs,
    )


def f_math_cos(inter, line, args, **kwargs):
    import math
    return _try_math(
        inter,
        lambda: math.cos(inter.parse(0, line, args)[2]),
        line,
        **kwargs,
    )


def f_math_tan(inter, line, args, **kwargs):
    import math
    return _try_math(
        inter,
        lambda: math.tan(inter.parse(0, line, args)[2]),
        line,
        **kwargs,
    )


def f_math_asin(inter, line, args, **kwargs):
    import math
    return _try_math(
        inter,
        lambda: math.asin(inter.parse(0, line, args)[2]),
        line,
        **kwargs,
    )


OBJ_MATH_TRIG_DISPATCH = {
    "sin": f_math_sin,
    "cos": f_math_cos,
    "tan": f_math_tan,
    "asin": f_math_asin,
}
