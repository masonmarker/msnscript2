

from core.classes.var import Var

def f_do(inter, line: str, args, **kwargs):
    ret = inter.parse(0, line, args)[2]
    inter.interpret(args[1][0])
    return ret

def f_as(inter, line, args, **kwargs):
    # temporary variable name
    varname = inter.parse(0, line, args)[2]
    # varname must be a varname
    inter.check_varname(varname, line)
    # block to execute
    block = args[2][0]
    # set the variable
    inter.vars[varname] = Var(varname, inter.parse(1, line, args)[2])
    # execute the block
    ret = inter.interpret(block)
    # delete the variable
    del inter.vars[varname]
    return ret

def f_varmethod(inter, line, args, **kwargs):
    # variable name
    return inter.interpret(
        f"{inter.parse(0, line, args)[2]}.{args[1][0]}"
    )

def f_try(inter, line, args, **kwargs):
    ret = None
    inter.trying = True
    try:
        ret = inter.interpret(args[0][0])
    except:
        inter.trying = False
        if len(args) == 2:
            ret = inter.interpret(args[1][0])
    inter.trying = False
    return ret

# multi-instruction function trigger
def f_multi_function(inter, line, args, **kwargs):
    from core.common import multi_lined
    return multi_lined(kwargs["inst"])

def f_eval(inter, line: str, args, **kwargs):
    arg = inter.parse(0, line, args)[2]
    # arg must be a str
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    return eval(arg)

LOGICAL_DISPATCH = {
    "do": f_do,
    "as": f_as,
    "varmethod": f_varmethod,
    "try": f_try,
    "=>": f_multi_function,
    "eval": f_eval,
}