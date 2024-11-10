



def f_py_else(inter, line: str, args, **kwargs):
    try:
        # check in locals
        return inter._locals[kwargs["objfunc"]]
    except KeyError:
        try:
            # check in globals
            return inter._globals[kwargs["objfunc"]]
        except Exception as e:
            # raise error
            inter.no_var_err(
                kwargs["objfunc"],
                "local or global",
                "local and global",
                inter._globals,
                line,
            )


OBJ_PY_DEFAULT_DISPATCH = {
    "else": f_py_else,
}