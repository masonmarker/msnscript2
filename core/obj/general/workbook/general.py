

from core.classes.excel.sheet import Sheet


def _prepare_workbook(inter, line, args, **kwargs):
    workbook = kwargs["object"].workbook
    path = kwargs["object"].path
    return workbook, path


def f_obj_general_workbook_sheet(inter, line, args, **kwargs):
    # prepare
    workbook, path = _prepare_workbook(inter, line, args, **kwargs)
    # sheet, either an integer or string
    sheet = inter.parse(0, line, args)[2]
    # sheet must be int or str
    inter.type_err([(sheet, (int, str))], line, kwargs["lines_ran"])
    # if number
    if isinstance(sheet, int):
        sheet += 1
        # get sheet by index
        for i, name in enumerate(workbook.sheetnames):
            if i == sheet:
                return Sheet(workbook[name], name, workbook, path)
    # otherwise, get sheet by title
    elif isinstance(sheet, str):
        # get sheet by title
        for name in workbook.sheetnames:
            if name.lower() == sheet.lower():
                return Sheet(workbook[name], name, workbook, path)
    return


def f_obj_general_workbook_save(inter, line, args, **kwargs):
    # prepare
    workbook, path = _prepare_workbook(inter, line, args, **kwargs)
    # save the workbook
    workbook.save(path)
    return kwargs["object"]


def f_obj_general_workbook_close(inter, line, args, **kwargs):
    # prepare
    workbook, path = _prepare_workbook(inter, line, args, **kwargs)
    # close the workbook
    workbook.close()
    return kwargs["object"]


OBJ_GENERAL_WORKBOOK_GENERAL_DISPATCH = {
    "sheet": f_obj_general_workbook_sheet,
    "save": f_obj_general_workbook_save,
    "close": f_obj_general_workbook_close,
}
