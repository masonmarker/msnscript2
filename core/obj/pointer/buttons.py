

from core.common import aliases


def f_pointer_click(inter, line, args, **kwargs):
    from pywinauto import mouse
    if len(args) == 2:
        return mouse.click(
            coords=(
                inter.parse(0, line, args)[2],
                inter.parse(1, line, args)[2],
            )
        )
    else:
        import win32api
        return mouse.click(coords=win32api.GetCursorPos())


def f_pointer_right_click(inter, line, args, **kwargs):
    # if args are provided
    if len(args) == 2:
        from pywinauto import mouse
        start = inter.parse(0, line, args)[2]
        # start must be int
        inter.type_err([(start, (int,))], line, kwargs["lines_ran"])
        end = inter.parse(1, line, args)[2]
        # end must be int
        inter.type_err([(end, (int,))], line, kwargs["lines_ran"])
        return mouse.right_click(coords=(start, end))
    # if no args are provided
    else:
        import win32api
        return mouse.right_click(coords=win32api.GetCursorPos())


def f_pointer_double_click(inter, line, args, **kwargs):
    # if args are provided
    if len(args) == 2:
        from pywinauto import mouse
        start = inter.parse(0, line, args)[2]
        # start must be int
        inter.type_err([(start, (int,))], line, kwargs["lines_ran"])
        end = inter.parse(1, line, args)[2]
        # end must be int
        inter.type_err([(end, (int,))], line, kwargs["lines_ran"])
        return mouse.double_click(coords=(start, end))
    # if no args are provided
    else:
        import win32api
        return mouse.double_click(coords=win32api.GetCursorPos())




def f_pointer_left_down(inter, line, args, **kwargs):
    import win32api
    return win32api.GetKeyState(0x01) < 0


def f_pointer_right_down(inter, line, args, **kwargs):
    import win32api
    return win32api.GetKeyState(0x02) < 0


def f_pointer_wait_left(inter, line, args, **kwargs):
    import win32api
    while True:
        if win32api.GetKeyState(0x01) < 0:
            break
    return True


def f_pointer_wait_right(inter, line, args, **kwargs):
    import win32api
    while True:
        if win32api.GetKeyState(0x02) < 0:
            break
    return True


def f_pointer_wait_left_click(inter, line, args, **kwargs):
    import win32api
    while True:
        if win32api.GetKeyState(0x01) < 0:
            break
    while True:
        if win32api.GetKeyState(0x01) >= 0:
            break
    return True


def f_pointer_wait_right_click(inter, line, args, **kwargs):
    import win32api
    while True:
        if win32api.GetKeyState(0x02) < 0:
            break
    while True:
        if win32api.GetKeyState(0x02) >= 0:
            break
    return True

OBJ_POINTER_BUTTONS_DISPATCH = {
    "right_click": f_pointer_right_click,
    "double_click": f_pointer_double_click,
    "left_down": f_pointer_left_down,
    "right_down": f_pointer_right_down,
    "wait_left_click": f_pointer_wait_left_click,
    "wait_right_click": f_pointer_wait_right_click,
    "wait_left": f_pointer_wait_left,
    "wait_right": f_pointer_wait_right,
    **aliases(f_pointer_click, ("click", "left_click")),
}
