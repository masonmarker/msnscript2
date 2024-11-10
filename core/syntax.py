

def f_syntax(inter, line, args, **kwargs):
    synt = inter.parse(0, line, args)[2]
    # synt must be str
    inter.type_err([(synt, (str,))], line, kwargs["lines_ran"])
    # add the between
    between = inter.parse(1, line, args)[2]
    # between must be a varname
    inter.check_varname(between, line)
    return inter.add_syntax(synt, between, args[2][0])


def f_enclosed_syntax(inter, line, args, **kwargs):
    start = inter.parse(0, line, args)[2]
    # start must be str
    inter.type_err([(start, (str,))], line, kwargs["lines_ran"])
    end = inter.parse(1, line, args)[2]
    # end must be str
    inter.type_err([(end, (str,))], line, kwargs["lines_ran"])
    varname = inter.parse(2, line, args)[2]
    # varname must be a varname
    inter.check_varname(varname, line)
    index = f"{start}msnint2_reserved{end}"
    kwargs["enclosed"][index] = [start, end, varname, args[3][0]]
    if len(args) == 5:
        kwargs["enclosed"][index].append(inter.parse(4, line, args)[2])
    return kwargs["enclosed"][index]


def f_macro(inter, line, args, **kwargs):
    token = inter.parse(0, line, args)[2]
    # token must be str
    inter.type_err([(token, (str,))], line, kwargs["lines_ran"])
    # get the symbol
    symbol = inter.parse(1, line, args)[2]
    # symbol must be str
    inter.type_err([(symbol, (str,))], line, kwargs["lines_ran"])
    kwargs["macros"][token] = [token, symbol, args[2][0]]
    # 4th argument offered as a return value from that macro
    # as opposed to a block of code
    if len(args) == 4:
        kwargs["macros"][token].append(inter.parse(3, line, args)[2])
    return kwargs["macros"][token]


def f_postmacro(inter, line, args, **kwargs):
    token = inter.parse(0, line, args)[2]
    # token must be str
    inter.type_err([(token, (str,))], line, kwargs["lines_ran"])
    # get the symbol
    symbol = inter.parse(1, line, args)[2]
    # symbol must be str
    inter.type_err([(symbol, (str,))], line, kwargs["lines_ran"])
    kwargs["postmacros"][token] = [token, symbol, args[2][0]]
    # same as macro
    if len(args) == 4:
        kwargs["postmacros"][token].append(inter.parse(3, line, args)[2])
    return kwargs["postmacros"][token]


SYNTAX_DISPATCH = {
    "syntax": f_syntax,
    "enclosedsyntax": f_enclosed_syntax,
    "macro": f_macro,
    "postmacro": f_postmacro,
}
