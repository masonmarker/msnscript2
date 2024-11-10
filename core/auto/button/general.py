

from core.common import aliases


def f_auto_button_click(inter, line, args, **kwargs):
    from core.auto.common import _prepare_button
    # preparing button
    window, p_thread = _prepare_button(inter, line, args, **kwargs)
    ret = kwargs["object"].click()
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_button_right_click(inter, line, args, **kwargs):
    from core.auto.common import _prepare_button
    window, p_thread = _prepare_button(inter, line, args, **kwargs)
    ret = kwargs["object"].right_click()
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


OBJ_GENERAL_BUTTON_GENERAL_DISPATCH = {
    "right_click": f_auto_button_right_click,
    **aliases(f_auto_button_click, ("click", "left_click")),
}
