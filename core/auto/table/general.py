

def row(index, table):
    from core.classes.auto.appelement import AppElement
    row = []
    items = []
    try:
        cols = table.column_count()
    except NotImplementedError:
        # not implemented
        cols = 5
        items = table.items()
    for i in range(cols):
        try:
            try:
                wrapper = table.cell(row=index, column=i)
            except:
                # table.items() gets a 1D list of items,
                # compute the index of the item
                # based on 'i' and 'index'
                wrapper = items[i + index * cols]

            row.append(
                AppElement(
                    wrapper, wrapper.window_text()
                )
            )
        except:
            break
    return row

# gets a column by index


def col(index, table):
    from core.classes.auto.appelement import AppElement
    col = []
    for i in range(table.column_count()):
        try:
            wrapper = table.cell(row=i, column=index)
            col.append(
                AppElement(
                    wrapper, wrapper.window_text()
                )
            )
        except:
            break
    return col


def f_auto_table_get(inter, line, args, **kwargs):
    from core.classes.auto.appelement import AppElement
    from core.auto.common import _prepare_table
    # prepare table
    window, table, p_thread = _prepare_table(inter, line, args, **kwargs)

    # main logic
    # get column
    col = inter.parse(0, line, args)[2]
    # get row
    row = inter.parse(1, line, args)[2]
    # column and row should be int
    inter.type_err(
        [(col, (int,)), (row, (int,))], line, kwargs["lines_ran"]
    )
    wrapper = table.cell(row=row, column=col)
    # gets the cell
    ret = AppElement(wrapper, wrapper.window_text())

    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_table_matrix(inter, line, args, **kwargs):
    from core.auto.common import _prepare_table
    # prepare table
    window, table, p_thread = _prepare_table(inter, line, args, **kwargs)

    # main logic
    import sys

    matrix = []
    for i in range(sys.maxsize):
        try:
            if _r := row(i, table):
                matrix.append(_r)
            else:
                break
        except:
            break
    ret = matrix

    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_table_row(inter, line, args, **kwargs):
    from core.auto.common import _prepare_table
    # prepare table
    window, table, p_thread = _prepare_table(inter, line, args, **kwargs)

    # main logic
    ind = inter.parse(0, line, args)[2]
    # ind should be int
    inter.type_err([(ind, (int,))], line, kwargs["lines_ran"])
    ret = row(ind, table)

    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_table_column(inter, line, args, **kwargs):
    from core.auto.common import _prepare_table
    # prepare table
    window, table, p_thread = _prepare_table(inter, line, args, **kwargs)

    # main logic
    ind = inter.parse(0, line, args)[2]
    # ind should be int
    inter.type_err([(ind, (int,))], line, kwargs["lines_ran"])
    ret = col(ind, table)

    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


OBJ_GENERAL_TABLE_GENERAL_DISPATCH = {
    "get": f_auto_table_get,
    "matrix": f_auto_table_matrix,
    "row": f_auto_table_row,
    "column": f_auto_table_column,
}
