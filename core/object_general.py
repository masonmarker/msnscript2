"""General object functions."""


from core.classes.var import RESERVED_VARNAME_PREFIX, Var


def f_copy(inter, line, args, **kwargs):
    try:
        return inter.parse(0, line, args)[2].copy()
    except Exception as e:
        return inter.err("Error copying object", e, line, kwargs["lines_ran"])


def f_type(inter, line, args, **kwargs):
    return type(inter.parse(0, line, args)[2])


def f_equals(inter, line, args, **kwargs):
    arg1 = inter.parse(0, line, args)[2]
    return all(
        inter.parse(i, line, args)[-1] == arg1
        for i in range(1, len(args))
    )


def f_class(inter, line, args, **kwargs):
    # new interpreter
    new_int = inter.new_int()
    # extract class name
    name = inter.parse(0, line, args)[2]
    # name must be a varname
    inter.check_varname(name, line)
    # execute the block in the private environment
    new_int.execute(args[1][0], include_temp_vars=False)
    # creates a variable out of the new interpreters resources
    obj_to_add = {}
    for varname in new_int.vars:
        if not varname.startswith(RESERVED_VARNAME_PREFIX):
            val = new_int.vars[varname].value
            obj_to_add[varname] = Var(varname, val)
    for methodname in new_int.methods:
        obj_to_add[methodname] = Var(
            f"{methodname}#method", new_int.methods[methodname]
        )
    inter.vars[name] = Var(name, obj_to_add)
    return obj_to_add


def f_static(inter, line, args, **kwargs):
    try:
        return inter.parse(0, line, args)[2].value
    except Exception as e:
        inter.err("Error in static()", e, line, kwargs["lines_ran"])


def f_getattr(inter, line, args, **kwargs):
    vn = inter.parse(0, line, args)[2]
    # vn must be a varname
    inter.check_varname(vn, line)
    # get the attribute
    return inter.vars[vn].value[inter.parse(1, line, args)[2]]


def f_setattr(inter, line, args, **kwargs):
    # current working object
    o = inter.vars[inter.parse(0, line, args)[2]].value
    # name of attribute to set
    attr = inter.parse(1, line, args)[2]
    # attr must be a string
    inter.type_err([(attr, (str,))], line, kwargs["lines_ran"])
    # value to set
    val = inter.parse(2, line, args)[2]
    # set the value
    o[attr] = val
    return val


OBJECT_GENERAL_DISPATCH = {
    "copy": f_copy,
    "type": f_type,
    "equals": f_equals,
    "class": f_class,
    "static": f_static,
    "getattr": f_getattr,
    "setattr": f_setattr,
}
