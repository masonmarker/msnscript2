
def f_function_getbody(inter, line, args, **kwargs):
    fname = inter.parse(0, line, args)[2]
    # fname must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    return inter.methods[fname].body


def f_function_getargs(inter, line, args, **kwargs):
    fname = inter.parse(0, line, args)[2]
    # fname must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    return inter.methods[fname].args


def f_function_getreturn(inter, line, args, **kwargs):
    fname = inter.parse(0, line, args)[2]
    # fname must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    return inter.methods[fname].returns[0]


OBJ_FUNCTION_ACCESS_DISPATCH = {
    "getbody": f_function_getbody,
    "getargs": f_function_getargs,
    "getreturn": f_function_getreturn,
}
