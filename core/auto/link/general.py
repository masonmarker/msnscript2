
from core.common import aliases


def f_auto_link_click(inter, line, args, **kwargs):
    from core.auto.common import _prepare_link, clk
    # prepare link
    window, waittime, p_thread = _prepare_link(inter, line, args, **kwargs)
    # click the link
    ret = clk(window, waittime=waittime)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_link_right_click(inter, line, args, **kwargs):
    from core.auto.common import _prepare_link, clk
    # prepare link
    window, waittime, p_thread = _prepare_link(inter, line, args, **kwargs)
    # right click the link
    ret = clk(window, button="right", waittime=waittime)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


OBJ_GENERAL_LINK_GENERAL_DISPATCH = {
    "right_click": f_auto_link_right_click,
    **aliases(f_auto_link_click, ("click", "left_click")),
}
