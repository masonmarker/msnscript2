

def f_pointer_scroll_bottom(inter, line, args, **kwargs):
    import win32api
    from pywinauto import mouse
    return mouse.scroll(
        wheel_dist=9999999, coords=win32api.GetCursorPos()
    )


def f_pointer_scroll_top(inter, line, args, **kwargs):
    import win32api
    from pywinauto import mouse
    return mouse.scroll(
        wheel_dist=-9999999, coords=win32api.GetCursorPos()
    )


def f_pointer_scroll(inter, line, args, **kwargs):
    import win32api
    from pywinauto import mouse
    dist = inter.parse(0, line, args)[2]
    # dist must be int
    inter.type_err([(dist, (int,))], line, kwargs["lines_ran"])
    return mouse.scroll(
        wheel_dist=dist, coords=win32api.GetCursorPos()
    )


OBJ_POINTER_SCROLLING_DISPATCH = {
    "scroll_bottom": f_pointer_scroll_bottom,
    "scroll_top": f_pointer_scroll_top,
    "scroll": f_pointer_scroll,
}
