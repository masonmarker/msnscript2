

from core.obj.general.sheet.common import _prepare_sheet, get_column_index, get_row_index


def f_obj_general_sheet_set(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # column of the cell
    column = inter.parse(0, line, args)[2]
    # row of the cell
    row = inter.parse(1, line, args)[2]
    # row and column must be int
    inter.type_err(
        [(column, (int,)), (row, (int,))], line, kwargs["lines_ran"]
    )
    # value to set the cell to
    value = inter.parse(2, line, args)[2]
    # sets the value of the cell
    sheet.cell(row + 1, column + 1, value)
    # returns the sheet
    return value

def f_obj_general_sheet_clear(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # clears the sheet
    for row in sheet.iter_rows():
        for cell in row:
            cell.value = None
    # returns the sheet
    return kwargs["object"]

def f_obj_general_sheet_set_column(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # column, either an integer or string
    col = inter.parse(0, line, args)[2]
    # col must be int or str
    inter.type_err([(col, (int, str))], line, kwargs["lines_ran"])
    # iterable of values
    values = inter.parse(1, line, args)[2]
    # check that values is an iterable
    inter.check_iterable(values, line)
    # if number
    if isinstance(col, int):
        col += 1
        for i in range(len(values)):
            sheet.cell(i + 1, col, values[i])
    # otherwise, get column by title
    elif isinstance(col, str):
        # for each column
        for cell in sheet.iter_cols():
            # if the title matches
            if cell[0].value == col:
                # get the column values
                for i in range(len(values)):
                    sheet.cell(
                        i + 1, get_column_index(col, sheet), values[i]
                    )
    return values
def f_obj_general_sheet_set_row(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # row, either an integer or string
    r = inter.parse(0, line, args)[2]
    # must be int or str
    inter.type_err([(r, (int, str))], line, kwargs["lines_ran"])
    # array of values
    values = inter.parse(1, line, args)[2]
    # check that values is an iterable
    inter.check_iterable(values, line)
    # if number
    if isinstance(r, int):
        r += 1
        for i in range(len(values)):
            sheet.cell(r, i + 1, values[i])
    # otherwise, get row by title
    elif isinstance(r, str):
        # for each row
        for cell in sheet.iter_rows():
            # if the title matches
            if cell[0].value == r:
                # get the row values
                for i in range(len(values)):
                    sheet.cell(
                        get_row_index(r, sheet), i + 1, values[i]
                    )
    return values

def f_obj_general_sheet_add_to_column(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # column
    column = inter.parse(0, line, args)[2]
    # column should be an int or str
    inter.type_err([(column, (int, str))], line, kwargs["lines_ran"])
    # value to add
    value = inter.parse(1, line, args)[2]
    # if number
    if isinstance(column, int):
        column += 1
        # find the first empty cell in the column
        for i in range(sheet.max_row + 1):
            if sheet.cell(i + 1, column).value is None:
                sheet.cell(i + 1, column, value)
                return value
        return value
    # otherwise, get column by title
    elif isinstance(column, str):
        column_index = get_column_index(column, sheet)
        # find the first empty cell in the column
        for i in range(sheet.max_row + 1):
            if sheet.cell(i + 1, column_index).value is None:
                sheet.cell(i + 1, column_index, value)
                return value
    return value


def f_obj_general_sheet_add_to_row(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # row
    row = inter.parse(0, line, args)[2]
    # row should be an int or str
    inter.type_err([(row, (int, str))], line, kwargs["lines_ran"])
    # value to add
    value = inter.parse(1, line, args)[2]
    # if number
    if isinstance(row, int):
        row += 1
        # find the first empty cell in the row
        for i in range(sheet.max_column):
            if sheet.cell(row, i + 1).value is None:
                sheet.cell(row, i + 1, value)
                return value
        return value
    # otherwise, get row by title
    elif isinstance(row, str):
        row_index = get_row_index(row, sheet)
        # find the first empty cell in the row
        for i in range(sheet.max_column):
            if sheet.cell(row_index, i + 1).value is None:
                sheet.cell(row_index, i + 1, value)
                return value
    return value
def f_obj_general_sheet_import_matrix(inter, line, args, **kwargs):
    # prepare
    title, workbook, path, sheet = _prepare_sheet(inter, line, args, **kwargs)
    # get the 2D list
    matrix = inter.parse(0, line, args)[2]
    # matrix must be a list
    inter.type_err([(matrix, (list,))], line, kwargs["lines_ran"])
    # default offset
    offsetx = 0
    offsety = 0
    # if there is a second argument
    if len(args) == 2:
        offsetx = inter.parse(1, line, args)[2]
    if len(args) == 3:
        offsetx = inter.parse(1, line, args)[2]
        offsety = inter.parse(2, line, args)[2]
    # for each row
    for i in range(len(matrix)):
        # for each column
        for j in range(len(matrix[i])):
            w = matrix[i][j]
            # if w is an AppElement, write its name
            if "name" in dir(w):
                w = w.name
            sheet.cell(i + offsety + 1, j + offsetx + 1, w)
    return matrix

OBJ_GENERAL_SHEET_MODIFY_DISPATCH = {
    "set": f_obj_general_sheet_set,
    "clear": f_obj_general_sheet_clear,
    "set_column": f_obj_general_sheet_set_column,
    "set_row": f_obj_general_sheet_set_row,
    "add_to_column": f_obj_general_sheet_add_to_column,
    "add_to_row": f_obj_general_sheet_add_to_row,
    "import_matrix": f_obj_general_sheet_import_matrix,
}