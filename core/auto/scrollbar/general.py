



def f_auto_scrollbar_scroll_down(inter, line, args, **kwargs):
    from core.auto.common import _prepare_scrollbars
    
    # prepare scrollbar
    window, p_thread = _prepare_scrollbars(inter, line, args, **kwargs)

    # main logic
    ret = kwargs["object"].window.scroll_down(amount="page", count=1)

    # unlock threads
    if p_thread:
        kwargs["auto_lock"].release()
    return ret



OBJ_GENERAL_SCROLLBAR_GENERAL_DISPATCH = {
    "scroll_down": f_auto_scrollbar_scroll_down,
}
