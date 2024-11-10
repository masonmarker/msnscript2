"""Function-based dispatch functions."""


from core.classes.var import Var

def f_function(inter, line: str, args, **kwargs):
    from core.classes.method import Method
    # obtain the name of the function
    fname = inter.parse(0, line, args)[2]
    # function name must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    # function arguments
    # create the new Method
    new_method = Method(fname, inter)
    # add the body
    new_method.add_body(args[1][0])
    new_method.add_return(f"{fname}__return__")
    # obtain the rest of the arguments as method args
    for i in range(2, len(args)):
        # adds variable name as an argument
        # if any function specific argument is None, break
        val = inter.parse(i, line, args)[2]
        # val must be a string
        inter.type_err([(val, (str,))], line, kwargs["lines_ran"])
        if val is None:
            break
        new_method.add_arg(val)
    inter.methods[fname] = new_method
    return fname
def user_function_exec(inst, lines_ran):
    from core.classes.var import Var
    method = inst.interpreter.methods[inst.func]
    # create func args
    func_args = []
    # if arguments supplied
    if not inst.args[0][0] == '':
        for i in range(len(inst.args)):
            # check if we're setting a certain argument
            as_s = inst.args[i][0].strip()
            meth_argname = None
            if as_s[0] == '&':
                func_args, meth_argname, arg, ind = inst.interpreter.split_named_arg(
                    as_s, method, func_args, user_func=True)
            # else, just append the argument
            else:
                arg = inst.parse(i)
                func_args.append(arg)
            try:
                meth_argname = method.args[i]
            # incorrect amount of function arguments supplied
            except IndexError:
                inst.interpreter.raise_incorrect_args(str(len(method.args)), str(
                    inst.interpreter.arg_count(inst.args)), inst.line, lines_ran, method)
            try:
                inst.interpreter.vars[meth_argname] = Var(
                    meth_argname, arg)
            # unhashable type:list, this means a named argument
            # is being requested to be set
            except TypeError:
                inst.interpreter.vars[meth_argname[0]] = Var(
                    meth_argname[0], arg)
    # create return variable
    ret_name = method.returns[0]
    # add the return variable if not exists
    if ret_name not in inst.interpreter.vars:
        inst.interpreter.vars[ret_name] = Var(ret_name, None)
    # execute method
    try:
        method.run(func_args, inst.interpreter, inst.args)
    # index out of bounds error in method run
    except IndexError:
        # raise msn2 error
        inst.interpreter.raise_index_out_of_bounds(
            inst.line, lines_ran, method)
    # if its a variable
    if ret_name in inst.interpreter.vars:
        return inst.interpreter.vars[ret_name].value
    try:
        return eval(str(inst.interpreter.vars[ret_name].value), {}, {})
    except:
        pass
    try:
        return str(inst.interpreter.vars[ret_name].value)
    except:
        return str(inst.interpreter.vars[ret_name])



def define(inst, lines_ran):
    from core.classes.method import Method
    # get the name of the new function
    name = inst.parse(0)
    # function name must be a string
    inst.type_err([(name, (str,))], lines_ran)
    # create the new function
    new_func = Method(name, inst.interpreter)
    func_args = []
    # __temp = self.Method('', self)
    __temp = Method('', inst.interpreter)
    # get the args for this function between the name and the body
    # parse all args between the name and the body
    for i in range(1, len(inst.args) - 1):
        # get the stripped string rep of this arg
        as_s = inst.args[i][0].strip()
        if as_s[0] == '&':
            func_args, meth_argname, _, ind = inst.interpreter.split_named_arg(
                as_s, __temp, func_args)
            # add argument with default value
            new_func.add_arg([meth_argname, func_args[ind]])
        else:
            # add this argument to the method
            new_func.add_arg(inst.parse(i))
            new_arg = inst.parse(i)
            # self.type_err([(new_arg, (str,))], line, lines_ran)
            inst.type_err([(new_arg, (str,))], lines_ran)
    # add the body
    new_func.add_body(f"ret('{name}',{inst.args[-1][0]})")
    # return buffer variable name
    r_name = f"{name}__return__"
    # if the return buffer doesn't exist, create it
    if r_name not in inst.interpreter.vars:
        from core.classes.var import Var
        # create the return variable
        inst.interpreter.vars[r_name] = Var(r_name, None)
    # add the return variable
    new_func.add_return(r_name)
    # add the function to the methods
    inst.interpreter.methods[name] = new_func
    # return the name of the function
    return name
def f_def(inter, line: str, args, **kwargs):
    return define(kwargs["inst"], kwargs["lines_ran"])

def f_ret(inter, line: str, args, **kwargs):
    name = inter.parse(0, line, args)[2]
    # name must be a string
    inter.type_err([(name, (str,))], line, kwargs["lines_ran"])
    # function to return to
    vname = f"{name}__return__"
    # value
    value = inter.parse(1, line, args)[2]
    # if the variable does not exist, we should create it
    if vname not in inter.vars:
        inter.vars[vname] = Var(vname, None)
    inter.vars[vname].value = value
    return value


def f_exists_function(inter, line: str, args, **kwargs):
    arg = inter.parse(0, line, args)[2]
    # arg must be str
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    return arg in inter.methods


def f_destroy_function(inter, line, args, **kwargs):
    fname = None
    for i in range(len(args)):
        fname = inter.parse(i, line, args)[2]
        # must be a varname
        inter.check_varname(fname, line)
        inter.methods.pop(fname)
    return fname

def f_return(inter, line, args, **kwargs):
    method = inter.methods[inter.loggedmethod[-1]]
    # evaluate returning literal
    ret = inter.parse(0, line, args)[2]
    # set return variable
    ret_name = method.returns[0]
    # if not a variable
    if ret_name not in inter.vars:
        inter.vars[ret_name] = Var(ret_name, None)
    inter.vars[ret_name].value = ret
    return ret

def f_end(inter, line, args, **kwargs):
    method = inter.methods[inter.loggedmethod[-1]]
    inter.loggedmethod.pop()
    method.ended = True
    return True

FUNCTION_BASED_DISPATCH = {
    "function": f_function,
    "def": f_def,
    "ret": f_ret,
    "exists:function": f_exists_function,
    "destroy:function": f_destroy_function,
    "return": f_return,
    "end": f_end
}