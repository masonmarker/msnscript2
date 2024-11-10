

def _prepare_sheet(inter, line, args, **kwargs):
    title = kwargs["object"].title
    workbook = kwargs["object"].workbook
    path = kwargs["object"].path
    sheet = kwargs["object"].sheet
    return title, workbook, path, sheet


# gets the index of a column with a given title
def get_column_index(title, sheet):
    for cell in sheet.iter_cols():
        if cell[0].value == title:
            return cell[0].column
    return

def get_row_index(title, sheet):
    for cell in sheet.iter_rows():
        if cell[0].value == title:
            return cell[0].row
    return