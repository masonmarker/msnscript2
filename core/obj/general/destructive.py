


def f_obj_general_destructive(inter, line, args, **kwargs):
    # recreate the line to interpret without the '!'
    inter.vars[kwargs["vname"]].value = inter.interpret(
        f"{kwargs['vname']}.{kwargs['objfunc'][:-1]}({kwargs['mergedargs']})"
    )
    return inter.vars[kwargs["vname"]].value


OBJ_GENERAL_DESTRUCTIVE_DISPATCH = {
    "!": f_obj_general_destructive
}