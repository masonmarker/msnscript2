

from core.obj.math.common import _try_math



def f_math_subtract(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: inter.parse(0, line, args)[2] - inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )


def f_math_multiply(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: inter.parse(0, line, args)[2] * inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )


def f_math_divide(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: inter.parse(0, line, args)[2] / inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )


def f_math_add(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: inter.parse(0, line, args)[2] + inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )

def f_math_mod(inter, line, args, **kwargs):
    return _try_math(
        inter,
        lambda: inter.parse(0, line, args)[2] % inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )
OBJ_MATH_BASIC_DISPATCH = {
    "add": f_math_add,
    "subtract": f_math_subtract,
    "multiply": f_math_multiply,
    "divide": f_math_divide,
    "mod": f_math_mod,
}
