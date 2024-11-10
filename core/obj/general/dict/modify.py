
from core.classes.var import Var


def f_obj_dict_set(inter, line, args, **kwargs):
    inter.vars[kwargs["vname"]].value[inter.parse(0, line, args)[2]] = inter.parse(1, line, args)[2]
    return inter.vars[kwargs["vname"]].value
def f_obj_dict_setn(inter, line, args, **kwargs):
    # what to set
    to_set = inter.parse(0, line, args)[2]
    # the rest of the arguments are the indices
    # example: dict.setn('im being set', 'index1', 'index2', 'index3', ...)
    # should equal: dict['index1']['index2']['index3'] = 'im being set'
    # the object to set
    obj = inter.vars[kwargs["vname"]].value
    # iterates through the indices
    for i in range(1, len(args)):
        # if the index is the last one
        if i == len(args) - 1:
            # sets the index to to_set
            obj[inter.parse(i, line, args)[2]] = to_set
        # if the index is not the last one
        else:
            # sets the object to the index
            obj = obj[inter.parse(i, line, args)[2]]
    # returns the object
    return inter.vars[kwargs["vname"]].value

def f_obj_dict_foreach(inter, line, args, **kwargs):
    # variable name of the key
    keyname = inter.parse(0, line, args)[2]
    # variable name of the value
    valuename = inter.parse(1, line, args)[2]
    # check both keyname and valuename as varnames
    inter.check_varname(keyname, line)
    inter.check_varname(valuename, line)
    # function to execute
    function = args[2][0]
    # loop through the dictionary
    for key, value in inter.vars[kwargs["vname"]].value.items():
        # set the key and value variables
        inter.vars[keyname] = Var(keyname, key)
        inter.vars[valuename] = Var(valuename, value)
        # execute the function
        inter.interpret(function)
    # return the dictionary
    return inter.vars[kwargs["vname"]].value
def f_obj_dict_map(inter, line, args, **kwargs):
    # map arguments
    keyvarname = inter.parse(0, line, args)[2]
    valuevarname = inter.parse(1, line, args)[2]
    # check both for varnames
    inter.check_varname(keyvarname, line)
    inter.check_varname(valuevarname, line)
    function = args[2][0]
    new_dict = {}
    # loop through the objects items, assigning the key to the key and
    # value to the value
    for key, value in inter.vars[kwargs["vname"]].value.items():
        # log old key
        old_key = key
        # execute the function
        inter.vars[keyvarname] = Var(keyvarname, key)
        inter.vars[valuevarname] = Var(valuevarname, value)
        # run the function
        ret = inter.interpret(function)
        if inter.vars[keyvarname].value == old_key:
            new_dict[old_key] = inter.vars[valuevarname].value
        else:
            new_dict[inter.vars[keyvarname].value] = inter.vars[valuevarname].value
    inter.vars[kwargs["vname"]].value = new_dict
    return inter.vars[kwargs["vname"]].value

OBJ_GENERAL_DICT_MODIFY_DISPATCH = {
    "set": f_obj_dict_set,
    "setn": f_obj_dict_setn,
    "foreach": f_obj_dict_foreach,
    "map": f_obj_dict_map,
}