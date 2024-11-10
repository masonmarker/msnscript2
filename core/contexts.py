
from core.classes.var import Var

from core.common import aliases


def f_new(inter, line, args, **kwargs):
    new_int = inter.new_int()
    return new_int.interpret(args[0][0])
def f_inheritmethods(inter, line, args, **kwargs):
    for methodname in inter.parent.methods:
        inter.methods[methodname] = inter.parent.methods[methodname]
    return True
def f_inheritvars(inter, line, args, **kwargs):
    for varname in inter.parent.vars:
        inter.vars[varname] = inter.parent.vars[varname]
    return True
def f_inheritsingle(inter, line, args, **kwargs):
    name = inter.parse(0, line, args)[2]
    # name must be a varname
    inter.check_varname(name, line)
    if name in inter.parent.vars:
        inter.vars[name] = inter.parent.vars[name]
    elif name in inter.parent.methods:
        inter.methods[name] = inter.parent.methods[name]
    return True
def f_export(inter, line, args, **kwargs):
    # if last argument is True,
    # we add the variables to the parent context's variable
    last_arg = inter.parse(len(args) - 1, line, args)[2]
    for i in range(len(args)):
        varname = inter.parse(i, line, args)[2]
        # varname must be a varname
        inter.check_varname(varname, line)
        if varname in inter.vars:
            if isinstance(last_arg, bool):
                # if inter.vars[varname].value is any type of number
                if isinstance(
                    inter.vars[varname].value, (int, float, complex)
                ):
                    inter.parent.vars[varname].value += inter.vars[
                        varname
                    ].value
                # otherwise add every element to the parent context's variable
                elif isinstance(inter.vars[varname].value, list):
                    for element in inter.vars[varname].value:
                        inter.parent.vars[varname].value.append(element)
            else:
                inter.parent.vars[varname] = inter.vars[varname]
        elif varname in inter.methods:
            inter.parent.methods[varname] = inter.methods[varname]
    return True
def f_exportas(inter, line, args, **kwargs):
    # variable name
    varname = inter.parse(0, line, args)[2]
    # varname must be a varname
    inter.check_varname(varname, line)
    # value
    val = inter.parse(1, line, args)[2]
    # export to parent context
    inter.parent.vars[varname] = Var(varname, val)
    return val
def f_exportall(inter, line, args, **kwargs):
    for varname in inter.vars:
        inter.parent.vars[varname] = inter.vars[varname]
    for methodname in inter.methods:
        inter.parent.methods[methodname] = inter.methods[methodname]
    return True
def f_exportthread(inter, line, args, **kwargs):
    # thread name
    tname = inter.parse(0, line, args)[2]
    # thread must exist
    if not (thread := inter.thread_by_name(tname)):
        inter.err(
            "Thread does not exist",
            f'Thread name "{tname}" does not exist in this context',
            line,
            kwargs["lines_ran"],
        )
    # export the thread to the parent context
    inter.parent.threads[tname] = inter.threads[tname]
    return tname
def f_private(inter, line, args, **kwargs):
    new_int = inter.new_int()
    for vname, entry in inter.vars.items():
        try:
            new_int.vars[vname] = Var(vname, entry.value, True)
        except:
            new_int.vars[vname] = Var(vname, entry, True)
    for mname, entry in inter.methods.items():
        new_int.methods[mname] = entry
    ret = new_int.interpret(args[0][0])
    return ret



CONTEXTS_DISPATCH = {
    "new": f_new,
    "inherit:methods": f_inheritmethods,
    "inherit:vars": f_inheritvars,
    "inherit:single": f_inheritsingle,
    "export": f_export,
    **aliases(f_private, ("private", "inherit:all")),
    **aliases(f_exportas, ("exportas", "export:as")),
    **aliases(f_exportall, ("exportall", "export:all")),
    **aliases(f_exportthread, ("exportthread", "export:thread")),  
}