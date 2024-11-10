

def _try_cast(inter, func, line: str, **kwargs):
    try:
        return func()
    except Exception as e:
        inter.err(
            "Casting error",
            f"Could not cast arg to specified type\n{e}",
            line,
            kwargs["lines_ran"],
        )
# casting functions


def f_int(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: int(inter.parse(0, line, args)[2]), line, **kwargs)


def f_float(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: float(inter.parse(0, line, args)[2]), line, **kwargs)


def f_str(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: str(inter.parse(0, line, args)[2]), line, **kwargs)


def f_bool(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: bool(inter.parse(0, line, args)[2]), line, **kwargs)


def f_complex(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: complex(inter.parse(0, line, args)[2]), line, **kwargs)


def f_type(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: type(inter.parse(0, line, args)[2]), line, **kwargs)


def f_dir(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: dir(inter.parse(0, line, args)[2]), line, **kwargs)


def f_set(inter, line: str, args, **kwargs):
    if args[0][0] == "":
        return set()
    s = set()
    for i in range(len(args)):
        s.add(inter.parse(i, line, args)[2])
    return s


def f_dict(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: dict(inter.parse(0, line, args)[2]), line, **kwargs)


def f_tuple(inter, line: str, args, **kwargs):
    return _try_cast(inter, lambda: tuple(inter.parse(0, line, args)[2]), line, **kwargs)


CAST_DISPATCH = {
    # casting functions
    "int": f_int,
    "float": f_float,
    "str": f_str,
    "bool": f_bool,
    "complex": f_complex,
    "type": f_type,
    "dir": f_dir,
    "set": f_set,
    "dict": f_dict,
    "tuple": f_tuple,
}
