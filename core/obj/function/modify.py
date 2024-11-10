

def f_function_addbody(inter, line, args, **kwargs):
    fname = inter.parse(0, line, args)[2]
    # fname must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    inter.methods[fname].add_body(inter.parse(1, line, args)[2])
    return fname


def f_function_addarg(inter, line, args, **kwargs):
    fname = inter.parse(0, line, args)[2]
    # fname must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    arg = inter.parse(1, line, args)[2]
    # arg must be a string
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    inter.methods[fname].add_arg(arg)
    return fname


def f_function_addreturn(inter, line, args, **kwargs):
    fname = inter.parse(0, line, args)[2]
    # fname must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    ret = inter.parse(1, line, args)[2]
    # ret must be a string
    inter.type_err([(ret, (str,))], line, kwargs["lines_ran"])
    inter.methods[fname].add_return(ret)
    return fname


def f_function_destroy(inter, line, args, **kwargs):
    fname = inter.parse(0, line, args)[2]
    # fname must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    inter.methods.pop(fname)
    return fname


OBJ_FUNCTION_MODIFY_DISPATCH = {
    "addbody": f_function_addbody,
    "addarg": f_function_addarg,
    "addreturn": f_function_addreturn,
    "destroy": f_function_destroy,
}
