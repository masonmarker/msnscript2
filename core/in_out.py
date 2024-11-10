# intaking system arguments / sending resources out

from core.classes.var import Var

def f_in(inter, line, args, **kwargs):
    reserved_name = "_msn2_reserved_in__"
    if reserved_name not in inter.vars:
        return None
    inval = inter.vars[reserved_name].value
    # if no arguments, return the value
    if args[0][0] == "":
        return inval
    # if 1 argument, get index of value from input
    elif len(args) == 1:
        ind = inter.parse(0, line, args)[2]
        # ind must be int
        inter.type_err([(ind, (int,))], line, kwargs["lines_ran"])
        return inval[ind]
    # if 2 arguments, get slice of input
    elif len(args) == 2:
        start = inter.parse(0, line, args)[2]
        # start must be int
        inter.type_err([(start, (int,))], line, kwargs["lines_ran"])
        end = inter.parse(1, line, args)[2]
        # end must be int
        inter.type_err([(end, (int,))], line, kwargs["lines_ran"])
        return inval[start:end]
    return inval
def f_out(inter, line, args, **kwargs):
    outting = [inter.parse(i, line, args)[2] for i in range(len(args))]
    reserved_name = "_msn2_reserved_out__"
    inter.vars[reserved_name] = Var(reserved_name, outting)
    return outting


IN_OUT_DISPATCH = {
    "in": f_in,
    "out": f_out,
}