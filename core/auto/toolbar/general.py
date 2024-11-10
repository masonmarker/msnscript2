

def f_auto_toolbar_buttons(inter, line, args, **kwargs):
    from core.auto.common import _prepare_toolbars
    # prepare toolbars
    toolbar_window, toolbars, p_thread = _prepare_toolbars(
        inter, line, args, **kwargs)
    ret = [
        toolbar_window.button(i)
        for i in range(toolbar_window.button_count())
    ]
    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_toolbar_button(inter, line, args, **kwargs):
    from core.auto.common import _prepare_toolbars
    # prepare toolbars
    toolbar_window, toolbars, p_thread = _prepare_toolbars(
        inter, line, args, **kwargs)
    ret = toolbar_window.button(
        inter.parse(0, line, args)[2]
    )
    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_toolbar_find_buttons(inter, line, args, **kwargs):
    from core.auto.common import _prepare_toolbars, find_buttons
    # prepare toolbars
    toolbar_window, toolbars, p_thread = _prepare_toolbars(
        inter, line, args, **kwargs)

    txt = inter.parse(0, line, args)[2]
    # txt should be str
    inter.type_err([(txt, (str,))], line, kwargs["lines_ran"])
    ret = find_buttons(toolbar_window, txt)

    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_toolbar_print_buttons(inter, line, args, **kwargs):
    from core.auto.common import _prepare_toolbars
    # prepare toolbars
    toolbar_window, toolbars, p_thread = _prepare_toolbars(
        inter, line, args, **kwargs)
    for i in range(toolbar_window.button_count()):
        print(i, ":", toolbar_window.button(i))
    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return None


OBJ_GENERAL_TOOLBAR_GENERAL_DISPATCH = {
    "buttons": f_auto_toolbar_buttons,
    "button": f_auto_toolbar_button,
    "find_buttons": f_auto_toolbar_find_buttons,
    "print_buttons": f_auto_toolbar_print_buttons,
}
