


def f_function_run(inter, line, args, **kwargs):
    fname = inter.parse(0, line, args)[2]
    # fname must be a string
    inter.type_err([(fname, (str,))], line, kwargs["lines_ran"])
    # form a string that is msn2 of the user defined function
    args_str = ""
    for i in range(1, len(args)):
        arg = inter.parse(i, line, args)[2]
        if i != len(args) - 1:
            args_str += f"{arg},"
        else:
            args_str += str(arg)
    inst = f"{fname}({args_str})"
    return inter.interpret(inst)



OBJ_FUNCTION_RUN_DISPATCH = {
    "run": f_function_run,
}