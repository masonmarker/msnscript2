

def f_obj_general_workbook_default(inter, line, args, **kwargs):
    return kwargs["object"]


OBJ_GENERAL_WORKBOOK_DEFAULT_DISPATCH = {
    "else": f_obj_general_workbook_default,
}
