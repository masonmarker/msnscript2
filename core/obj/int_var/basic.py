


def f_var_equals(inter, line, args, **kwargs):
    firstvar = inter.parse(0, line, args)[2]
    return all(
        firstvar == inter.parse(i, line, args)[2]
        for i in range(1, len(args))
    )


OBJ_INT_VAR_BASIC_DISPATCH = {
    "equals": f_var_equals,
}