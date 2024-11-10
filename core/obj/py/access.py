


def f_py_get(inter, line: str, args, **kwargs):
    vn = ""
    name = inter.parse(0, line, args)[2]
    # name must be str
    inter.type_err([(name, (str,))], line, kwargs["lines_ran"])
    try:
        return inter._locals[name]
    except KeyError:
        inter.no_var_err(vn, "local", "local", inter._locals, line)


def f_py_set(inter, line: str, args, **kwargs):
    # name
    vn = inter.parse(0, line, args)[2]
    # vn must be str
    inter.type_err([(vn, (str,))], line, kwargs["lines_ran"])
    value = inter.parse(1, line, args)[2]
    inter._locals[vn] = value
    return value


def f_py_locals(inter, line: str, args, **kwargs):
    return inter._locals


def f_py_local(inter, line: str, args, **kwargs):
    vn = inter.parse(0, line, args)[2]
    # vn must be str
    inter.type_err([(vn, (str,))], line, kwargs["lines_ran"])
    try:
        return inter._locals[vn]
    except KeyError:
        inter.no_var_err(vn, "local", "local", inter._locals, line)


def f_py_globals(inter, line: str, args, **kwargs):
    return inter._globals


def f_py_global(inter, line: str, args, **kwargs):
    vn = inter.parse(0, line, args)[2]
    # vn must be str
    inter.type_err([(vn, (str,))], line, kwargs["lines_ran"])
    try:
        return inter._globals[vn]
    except:
        inter.no_var_err(vn, "global", "global", inter._globals, line)




OBJ_PY_ACCESS_DISPATCH = {
    "get": f_py_get,
    "set": f_py_set,
    "locals": f_py_locals,
    "local": f_py_local,
    "globals": f_py_globals,
    "global": f_py_global,
}