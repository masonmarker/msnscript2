

       
# seperate set of functions for creating object instances
def f_instance_new(inter, line, args, **kwargs):
    from core.classes.method import Method
    classname = kwargs["func"]
    # template Var obj to create from
    var_obj = inter.vars[classname].value
    instance = {}
    curr_arg_num = 0
    # attributes to apply
    for name in var_obj:
        # if attribute is a method
        if isinstance(var_obj[name].value, Method):
            # add the method to the instance
            instance[name] = var_obj[name].value
            # if the method's name is 'const'
            if var_obj[name].value.name == "const":
                # run the function with the argument being
                # this instance
                var_obj[name].value.run(
                    [instance], inter, actual_args=args[1:]
                )
            continue
        # if attribute is a variable
        # value can be None
        try:
            instance[name] = inter.parse(curr_arg_num, line, args)[2]
            if instance[name] is None:
                instance[name] = var_obj[name].value
        # if not specified, field is default value
        except:
            try:
                instance[name] = var_obj.value[name].copy()
            except:
                instance[name] = var_obj[name].value
        curr_arg_num += 1
    return instance



OBJ_INSTANCE_CREATION_DISPATCH = {
    "new": f_instance_new,
}