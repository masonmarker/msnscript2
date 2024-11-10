




def f_obj_dict_get(inter, line, args, **kwargs):
    # the object to get from
    obj = inter.vars[kwargs["vname"]].value
    # iterates through the indices
    for i in range(len(args)):
        ind = inter.parse(i, line, args)[2]
        try:
            # sets the object to the index
            obj = obj[ind]
        except KeyError:
            inter.raise_key(ind, line)
    # returns the object
    return obj
def f_obj_dict_keys(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.keys()
def f_obj_dict_values(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.values()
def f_obj_dict_items(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.items()
OBJ_GENERAL_DICT_ACCESS_DISPATCH = {
    "get": f_obj_dict_get,
    "keys": f_obj_dict_keys,
    "values": f_obj_dict_values,
    "items": f_obj_dict_items,
}