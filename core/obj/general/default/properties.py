
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

def f_obj_default_val(inter, line, args, **kwargs):
    return kwargs["object"]
def f_obj_default_type(inter, line, args, **kwargs):
    return _try_obj_default_cast(
        inter,
        lambda: type(kwargs["object"]),
        kwargs["object"],
        line,
        kwargs["lines_ran"],
    )
def f_obj_default_len(inter, line, args, **kwargs):
    return _try_obj_default_cast(
        inter,
        lambda: len(kwargs["object"]),
        kwargs["object"],
        line,
        kwargs["lines_ran"],
    )

OBJ_GENERAL_DEFAULT_PROPERTIES_DISPATCH = {
    "val": f_obj_default_val,
    "type": f_obj_default_type,
    "len": f_obj_default_len,
}
