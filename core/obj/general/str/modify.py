




def f_obj_str_add(inter, line, args, **kwargs):
    for i in range(len(args)):
        adding = inter.parse(i, line, args)[2]
        # adding must be a string
        inter.type_err([(adding, (str,))], line, kwargs["lines_ran"])
        inter.vars[kwargs["vname"]].value += adding
    return inter.vars[kwargs["vname"]].value
def f_obj_str_split(inter, line, args, **kwargs):
    splitting_by = inter.parse(0, line, args)[2]
    # splitting_by must be a string
    inter.type_err([(splitting_by, (str,))], line, kwargs["lines_ran"])
    return inter.vars[kwargs["vname"]].value.split(splitting_by)

def f_obj_str_lwordremove(inter, line, args, **kwargs):
    # number of words to remove
    num = inter.parse(0, line, args)[2]
    # num must be an int
    inter.type_err([(num, (int,))], line, kwargs["lines_ran"])
    # number cannot be negative
    if num < 0:
        inter.err(
            "Value error",
            "Number of words to remove cannot be negative.",
            line,
            kwargs["lines_ran"],
        )
    # remove the words
    inter.vars[kwargs["vname"]].value = " ".join(
        inter.vars[kwargs["vname"]].value.split(" ")[num:]
    )
    return inter.vars[kwargs["vname"]].value
def f_obj_str_rwordremove(inter, line, args, **kwargs):
    # number of words to remove
    num = inter.parse(0, line, args)[2]
    # num must be an int
    inter.type_err([(num, (int,))], line, kwargs["lines_ran"])
    # number cannot be negative
    if num < 0:
        inter.err(
            "Value error",
            "Number of words to remove cannot be negative.",
            line,
            kwargs["lines_ran"],
        )
    # remove the words
    inter.vars[kwargs["vname"]].value = " ".join(
        inter.vars[kwargs["vname"]].value.split(" ")[:-num]
    )
    return inter.vars[kwargs["vname"]].value
def f_obj_str_replace(inter, line, args, **kwargs):
    # what to replace
    replacing = inter.parse(0, line, args)[2]
    wth = inter.parse(1, line, args)[2]
    # both must be strings
    inter.type_err(
        [(replacing, (str,)), (wth, (str,))], line, kwargs["lines_ran"]
    )
    # replacing with
    if len(args) == 2:
        # replaces all instances of replacing with wth
        inter.vars[kwargs["vname"]].value = inter.vars[kwargs["vname"]].value.replace(
            replacing, wth
        )
    elif len(args) == 3:
        third = inter.parse(2, line, args)[2]
        # third must be a string
        inter.type_err([(third, (str,))], line, kwargs["lines_ran"])
        inter.vars[kwargs["vname"]].value = inter.vars[kwargs["vname"]].value.replace(
            replacing, wth, third
        )
    # returns the new string
    return inter.vars[kwargs["vname"]].value
def f_obj_str_stripped(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.strip()
def f_obj_str_set(inter, line, args, **kwargs):
    # index to set
    index = inter.parse(0, line, args)[2]
    # index must be an int
    inter.type_err([(index, (int,))], line, kwargs["lines_ran"])
    # create a new string with the new character
    inter.vars[kwargs["vname"]].value = (
        f"{inter.vars[kwargs['vname']].value[:index]}{inter.parse(1, line, args)[2]}{inter.vars[kwargs['vname']].value[index + 1:]}"
    )
    # returns the new string
    return inter.vars[kwargs["vname"]].value
def f_obj_str_upper(inter, line, args, **kwargs):
    inter.vars[kwargs["vname"]].value = inter.vars[kwargs["vname"]].value.upper()
    return inter.vars[kwargs["vname"]].value
def f_obj_str_lower(inter, line, args, **kwargs):
    inter.vars[kwargs["vname"]].value = inter.vars[kwargs["vname"]].value.lower()
    return inter.vars[kwargs["vname"]].value
def f_obj_str_cut(inter, line, args, **kwargs):
    start = inter.parse(0, line, args)[2]
    end = inter.parse(1, line, args)[2]
    # both start and end must be ints
    inter.type_err(
        [(start, (int,)), (end, (int,))], line, kwargs["lines_ran"]
    )
    inter.vars[kwargs["vname"]].value = inter.vars[kwargs["vname"]].value[start:end]
    return inter.vars[kwargs["vname"]].value

def f_obj_str_shove(inter, line, args, **kwargs):
    inserting = inter.parse(0, line, args)[2]
    index = inter.parse(1, line, args)[2]
    # index must be an int
    inter.type_err([(index, (int,))], line, kwargs["lines_ran"])
    inter.vars[kwargs["vname"]].value = (
        f"{inter.vars[kwargs['vname']].value[:index]}{inserting}{inter.vars[kwargs['vname']].value[index:]}"
    )
    return inter.vars[kwargs["vname"]].value
def f_obj_str_around(inter, line, args, **kwargs):
    # keyword to search for
    keyword = inter.parse(0, line, args)[2]
    # keyword must be a string
    inter.type_err([(keyword, (str,))], line, kwargs["lines_ran"])
    # get the index of the keyword
    index = inter.vars[kwargs["vname"]].value.find(keyword)
    # if not found
    if index == -1:
        # f"around(): Keyword '{keyword}' not found in string"
        # raise an msn2 error
        inter.err(
            f"around(): Keyword '{keyword}' not found in string",
            line,
            kwargs["lines_ran"],
            kwargs["f"],
        )
    # get the string
    return kwargs["object"][
        index
        - inter.parse(1, line, args)[2] : index
        + len(keyword)
        + inter.parse(2, line, args)[2]
    ]
OBJ_GENERAL_STR_MODIFY_DISPATCH = {
    "add": f_obj_str_add,
    "split": f_obj_str_split,
    "lwordremove": f_obj_str_lwordremove,
    "rwordremove": f_obj_str_rwordremove,
    "replace": f_obj_str_replace,
    "stripped": f_obj_str_stripped,
    "set": f_obj_str_set,
    "upper": f_obj_str_upper,
    "lower": f_obj_str_lower,
    "cut": f_obj_str_cut,
    "shove": f_obj_str_shove,
    "around": f_obj_str_around,
}