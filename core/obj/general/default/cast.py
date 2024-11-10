

def _try_obj_default_cast(inter, func, object, line, lines_ran):
    try:
        return func()
    except:
        # no attribute func
        inter.err(
            "Casting error",
            f"Could not cast object of type {type(object)} to the type specified.",
            line,
            lines_ran,
        )

def f_obj_default_str(inter, line, args, **kwargs):
    return _try_obj_default_cast(
        inter,
        lambda: str(kwargs["object"]),
        kwargs["object"],
        line,
        kwargs["lines_ran"],
    )
def f_obj_default_int(inter, line, args, **kwargs):
    return _try_obj_default_cast(
        inter,
        lambda: int(kwargs["object"]),
        kwargs["object"],
        line,
        kwargs["lines_ran"],
    )
def f_obj_default_float(inter, line, args, **kwargs):
    return _try_obj_default_cast(
        inter,
        lambda: float(kwargs["object"]),
        kwargs["object"],
        line,
        kwargs["lines_ran"],
    )
def f_obj_default_complex(inter, line, args, **kwargs):
    return _try_obj_default_cast(
        inter,
        lambda: complex(kwargs["object"]),
        kwargs["object"],
        line,
        kwargs["lines_ran"],
    )
def f_obj_default_bool(inter, line, args, **kwargs):
    return _try_obj_default_cast(
        inter,
        lambda: bool(kwargs["object"]),
        kwargs["object"],
        line,
        kwargs["lines_ran"],
    )
def f_obj_default_dict(inter, line, args, **kwargs):
    return _try_obj_default_cast(
        inter,
        lambda: dict(kwargs["object"]),
        kwargs["object"],
        line,
        kwargs["lines_ran"],
    )






OBJ_GENERAL_DEFAULT_CAST_DISPATCH = {
    "str": f_obj_default_str,
    "int": f_obj_default_int,
    "float": f_obj_default_float,
    "complex": f_obj_default_complex,
    "bool": f_obj_default_bool,
    "dict": f_obj_default_dict,
}
