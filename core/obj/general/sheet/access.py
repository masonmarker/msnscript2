

from core.classes.var import Var
from core.obj.general.sheet.common import _prepare_sheet


def f_obj_general_sheet_get(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # column of the cell
    column = inter.parse(0, line, args)[2]
    # row of the cell
    row = inter.parse(1, line, args)[2]
    # returns the value of the cell
    return sheet.cell(row + 1, column + 1).value


def f_obj_general_sheet_column(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # column, either an integer or string
    col = inter.parse(0, line, args)[2]
    # col must be int or str
    inter.type_err([(col, (int, str))], line, kwargs["lines_ran"])
    column_values = []
    # if number
    if isinstance(col, int):
        col += 1
        column_values = [
            row.value
            for row in sheet.iter_rows(min_col=col, max_col=col)
            for row in row
            if row.value != None
        ]
    # otherwise, get column by title
    elif isinstance(col, str):
        # get all cell values in the column
        # having its first cell be == col
        column_values = []
        for row in sheet.iter_cols():
            if row[0].value == col:
                for cell in row:
                    if cell.value != None:
                        column_values.append(cell.value)
                break
    return column_values

def f_obj_general_sheet_row(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # row, either an integer or string
    r = inter.parse(0, line, args)[2]
    # r must be int or str
    inter.type_err([(r, (int, str))], line, kwargs["lines_ran"])
    row_values = []
    # if number
    if isinstance(r, int):
        r += 1
        row_values = [
            row.value
            for row in sheet.iter_rows(min_row=r, max_row=r)
            for row in row
            if row.value != None
        ]
    # otherwise, get row by title
    elif isinstance(r, str):
        # for each row
        row_values = []
        for row in sheet.iter_rows():
            if row[0].value == r:
                for cell in row:
                    if cell.value != None:
                        row_values.append(cell.value)
                break
    return row_values


def f_obj_general_sheet_each_row(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # variable
    row_var = inter.parse(0, line, args)[2]
    # check varname
    inter.check_varname(row_var, line)
    ret = None
    # for each cell
    for cell in sheet.iter_rows():
        # set the variable to the row
        inter.vars[row_var] = Var(
            row_var, [cell[i].value for i in range(len(cell))]
        )
        # execute the function
        ret = inter.interpret(args[1][0])
    return ret

OBJ_GENERAL_SHEET_ACCESS_DISPATCH = {
    "get": f_obj_general_sheet_get,
    "column": f_obj_general_sheet_column,
    "row": f_obj_general_sheet_row,
    "each_row": f_obj_general_sheet_each_row,
}