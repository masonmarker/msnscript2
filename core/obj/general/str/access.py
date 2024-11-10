


from core.common import aliases

def f_obj_str_lines(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.split("\n")
def f_obj_str_words(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.split(" ")

def f_obj_str_chars(inter, line, args, **kwargs):
    return list(inter.vars[kwargs["vname"]].value)
def f_obj_str_isdigit(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.isdigit()
def f_obj_str_isalpha(inter, line, args, **kwargs):
    return inter.vars[kwargs["vname"]].value.isalpha()
def f_obj_str_strip(inter, line, args, **kwargs):
    inter.vars[kwargs["vname"]].value = inter.vars[kwargs["vname"]].value.strip()
    return inter.vars[kwargs["vname"]].value
def f_obj_str_self(inter, line, args, **kwargs):
    try:
        return inter.vars[kwargs["vname"]].value
    except:
        return inter.vars[kwargs["vname"]]
def f_obj_str_get(inter, line, args, **kwargs):
    ind = inter.parse(0, line, args)[2]
    return inter.vars[kwargs["vname"]].value[ind]


def f_obj_str_startswith(inter, line, args, **kwargs):
    st = inter.parse(0, line, args)[2]
    # st must be a string
    inter.type_err([(st, (str,))], line, kwargs["lines_ran"])
    return inter.vars[kwargs["vname"]].value.startswith(st)
def f_obj_str_endswith(inter, line, args, **kwargs):
    st = inter.parse(0, line, args)[2]
    # st must be a string
    inter.type_err([(st, (str,))], line, kwargs["lines_ran"])
    return inter.vars[kwargs["vname"]].value.endswith(st)

OBJ_GENERAL_STR_ACCESS_DISPATCH = {
    "get": f_obj_str_get,
    "lines": f_obj_str_lines,
    "words": f_obj_str_words,
    "chars": f_obj_str_chars,
    "isdigit": f_obj_str_isdigit,
    "isalpha": f_obj_str_isalpha,
    "startswith": f_obj_str_startswith,
    "endswith": f_obj_str_endswith,
    "self": f_obj_str_self,
    **aliases(f_obj_str_strip, ("strip", "trim")),
}