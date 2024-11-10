

from core.common import aliases


def _try_op(inter, func, line, lines_ran):
    try:
        return func()
    except Exception as e:
        inter.err(
            "Error in op() class",
            f"Could not perform operation on arguments\n{e}",
            line,
            lines_ran,
        )


def f_op_append(inter, line, args, **kwargs):
    return _try_op(inter, lambda: _f_op_append(inter, line, args), line, kwargs["lines_ran"])


def _f_op_append(inter, line, args):
    arg1 = inter.parse(0, line, args)[2]
    if isinstance(arg1, list):
        for i in range(1, len(args)):
            arg1.append(inter.parse(i, line, args)[2])
        return arg1
    else:
        for i in range(1, len(args)):
            arg1 += inter.parse(i, line, args)[2]
        return arg1


def f_op_sub(inter, line, args, **kwargs):
    return _try_op(inter, lambda: _f_op_sub(inter, line, args), line, kwargs["lines_ran"])


def _f_op_sub(inter, line, args):
    arg1 = inter.parse(0, line, args)[2]
    for i in range(1, len(args)):
        arg1 -= inter.parse(i, line, args)[2]
    return arg1


def f_op_mul(inter, line, args, **kwargs):
    return _try_op(inter, lambda: _f_op_mul(inter, line, args), line, kwargs["lines_ran"])


def _f_op_mul(inter, line, args):
    arg1 = inter.parse(0, line, args)[2]
    for i in range(1, len(args)):
        arg1 *= inter.parse(i, line, args)[2]
    return arg1


def f_op_div(inter, line, args, **kwargs):
    return _try_op(inter, lambda: _f_op_div(inter, line, args), line, kwargs["lines_ran"])


def _f_op_div(inter, line, args):
    arg1 = inter.parse(0, line, args)[2]
    for i in range(1, len(args)):
        arg1 /= inter.parse(i, line, args)[2]
    return arg1


def f_op_idiv(inter, line, args, **kwargs):
    return _try_op(inter, lambda: _f_op_idiv(inter, line, args), line, kwargs["lines_ran"])


def _f_op_idiv(inter, line, args):
    arg1 = inter.parse(0, line, args)[2]
    for i in range(1, len(args)):
        arg1 //= inter.parse(i, line, args)[2]
    return arg1


def f_op_mod(inter, line, args, **kwargs):
    return _try_op(inter, lambda: _f_op_mod(inter, line, args), line, kwargs["lines_ran"])


def _f_op_mod(inter, line, args):
    arg1 = inter.parse(0, line, args)[2]
    for i in range(1, len(args)):
        arg1 %= inter.parse(i, line, args)[2]
    return arg1


def f_op_pow(inter, line, args, **kwargs):
    return _try_op(inter, lambda: _f_op_pow(inter, line, args), line, kwargs["lines_ran"])


def _f_op_pow(inter, line, args):
    arg1 = inter.parse(0, line, args)[2]
    for i in range(1, len(args)):
        arg1 **= inter.parse(i, line, args)[2]
    return arg1


def f_op_root(inter, line, args, **kwargs):
    return _try_op(inter, lambda: _f_op_root(inter, line, args), line, kwargs["lines_ran"])


def _f_op_root(inter, line, args):
    arg1 = inter.parse(0, line, args)[2]
    for i in range(1, len(args)):
        arg1 **= 1 / inter.parse(i, line, args)[2]
    return arg1

OBJ_OP_BASIC_DISPATCH = {
    **aliases(f_op_append, ("append", "push", "add", "plus", "+", "concat", "concatenate", "join", "merge", "sum")),
    **aliases(f_op_sub, ("sub", "minus", "subtract", "-")),
    **aliases(f_op_mul, ("mul", "times", "x", "*", "multiply")),
    **aliases(f_op_div, ("div", "divide", "over", "/")),
    **aliases(f_op_idiv, ("idiv", "intdiv", "intdivide", "intover", "//", "÷÷")),
    **aliases(f_op_mod, ("mod", "modulo", "modulus", "%", "remainder")),
    **aliases(f_op_pow, ("pow", "power", "exponent", "**")),
    **aliases(f_op_root, ("root", "nthroot", "nthrt")),
}
