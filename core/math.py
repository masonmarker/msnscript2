"""Math based functions."""

from core.common import hyphen

def _try_func_math(inter, func, line, **kwargs):
    try:
        return func()
    except Exception as e:
        return inter.err(
            "Error", e, line, kwargs["lines_ran"]
        )
def f_symbolminus(inter, line, args, **kwargs):
    return _try_func_math(
        inter,
        lambda: hyphen(**kwargs),
        line,
        **kwargs,
    )
def _f_plussymbol(inter, line, args, **kwargs):
    ret = inter.parse(0, line, args)[2]
    try:
        ret = ret.copy()
    except AttributeError:
        None
    for i in range(1, len(args)):
        ret += inter.parse(i, line, args)[2]
    return ret
def f_symbolplus(inter, line, args, **kwargs):
    return _try_func_math(
        inter,
        lambda: _f_plussymbol(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_symbolx(inter, line, args, **kwargs):
    ret = inter.parse(0, line, args)[2]
    try:
        ret = ret.copy()
    except AttributeError:
        None
    for i in range(1, len(args)):
        ret *= inter.parse(i, line, args)[2]
    return ret
def f_symbolx(inter, line, args, **kwargs):
    return _try_func_math(
        inter,
        lambda: _f_symbolx(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_symboldiv(inter, line, args, **kwargs):
    ret = inter.parse(0, line, args)[2]
    try:
        ret = ret.copy()
    except AttributeError:
        None
    for i in range(1, len(args)):
        ret /= inter.parse(i, line, args)[2]
    return ret
def f_symboldiv(inter, line, args, **kwargs):
    return _try_func_math(
        inter,
        lambda: _f_symboldiv(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_symboldivdiv(inter, line, args, **kwargs):
    ret = inter.parse(0, line, args)[2]
    try:
        ret = ret.copy()
    except AttributeError:
        None
    for i in range(1, len(args)):
        ret //= inter.parse(i, line, args)[2]
    return ret
def f_symboldivdiv(inter, line, args, **kwargs):
    return _try_func_math(
        inter,
        lambda: _f_symboldivdiv(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_symbolmod(inter, line, args, **kwargs):
    ret = inter.parse(0, line, args)[2]
    try:
        ret = ret.copy()
    except AttributeError:
        None
    for i in range(1, len(args)):
        ret %= inter.parse(i, line, args)[2]
    return ret
def f_symbolmod(inter, line, args, **kwargs):
    return _try_func_math(
        inter,
        lambda: _f_symbolmod(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
def _f_symbolpow(inter, line, args, **kwargs):
    ret = inter.parse(0, line, args)[2]
    try:
        ret = ret.copy()
    except AttributeError:
        None
    for i in range(1, len(args)):
        ret **= inter.parse(i, line, args)[2]
    return ret
def f_symbolpow(inter, line, args, **kwargs):
    return _try_func_math(
        inter,
        lambda: _f_symbolpow(inter, line, args, **kwargs),
        line,
        **kwargs,
    )
    
    
MATH_DISPATCH = {
    "-": f_symbolminus,
    "+": f_symbolplus,
    "x": f_symbolx,
    "*": f_symbolx,
    "/": f_symboldiv,
    "//": f_symboldivdiv,
    "%": f_symbolmod,
    "^": f_symbolpow,
}