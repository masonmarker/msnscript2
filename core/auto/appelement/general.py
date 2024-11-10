

from core.auto.common import rec
from core.common import aliases


def f_auto_appelement_window(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_text(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window.window_text()
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_top(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window.get_properties()["rectangle"].top
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_bottom(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window.get_properties()["rectangle"].bottom
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_left(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window.get_properties()["rectangle"].left
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_right(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window.get_properties()["rectangle"].right
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_center(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window.get_properties()["rectangle"].mid_point()
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_rectangle(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    r = window.get_properties()["rectangle"]
    ret = [
        r.top,
        r.bottom,
        r.left,
        r.right,
    ]
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_width(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    try:
        r = window.get_properties()["rectangle"]
        left = r.left
        right = r.right
        ret = right - left
    except:
        ret = None
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_height(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    try:
        r = window.get_properties()["rectangle"]
        top = r.top
        bottom = r.bottom
        ret = bottom - top
    except:
        ret = None
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_element_above(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret

    pixels = inter.parse(0, line, args)[2]
    inter.type_err([(pixels, (int,))], line, kwargs["lines_ran"])
    # get the root window of this application
    root = window.top_level_parent()
    # get the top middle point of this element
    r = window.get_properties()["rectangle"]
    top = r.top - pixels
    mid = r.mid_point()[0]
    # if there exist two arguments, move the mouse to that location
    if len(args) == 2:
        mouse.move(coords=(mid, top))
    # recursively find all children from the root window
    # that have the point specified
    ret = rec(root, mid, top)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_element_below(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret

    pixels = inter.parse(0, line, args)[2]
    inter.type_err([(pixels, (int,))], line, kwargs["lines_ran"])
    # get the root window of this application
    root = window.top_level_parent()
    # get the top middle point of this element
    r = window.get_properties()["rectangle"]
    bottom = r.bottom + pixels
    mid = r.mid_point()[0]
    if len(args) == 2:
        mouse.move(coords=(mid, bottom))
    # recursively find all children from the root window
    # that have the point specified
    ret = rec(root, mid, bottom)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_element_left(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret

    pixels = inter.parse(0, line, args)[2]
    inter.type_err([(pixels, (int,))], line, kwargs["lines_ran"])
    # get the root window of this application
    root = window.top_level_parent()
    # get the left middle point of this element
    r = window.get_properties()["rectangle"]
    left = r.left - pixels
    mid = r.mid_point()[1]
    if len(args) == 2:
        mouse.move(coords=(left, mid))
    # recursively find all children from the root window
    # that have the point specified
    ret = rec(root, left, mid)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_element_right(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret

    pixels = inter.parse(0, line, args)[2]
    inter.type_err([(pixels, (int,))], line, kwargs["lines_ran"])
    # get the root window of this application
    root = window.top_level_parent()
    # get the right middle point of this element
    r = window.get_properties()["rectangle"]
    right = r.right + pixels
    mid = r.mid_point()[1]
    if len(args) == 2:
        mouse.move(coords=(right, mid))
    # recursively find all children from the root window
    # that have the point specified
    ret = rec(root, right, mid)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_focus(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window.set_focus()
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_scroll(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    r = window.get_properties()["rectangle"]
    ret = mouse.scroll(
        coords=(
            r.mid_point()[0],
            r.mid_point()[1],
        )
    )
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_drag(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement, movemouse
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret

    first = inter.parse(0, line, args)[2]
    inter.type_err([(first, (inter.AppElement,))], line, kwargs["lines_ran"])
    r = window.get_properties()["rectangle"]
    start = (
        r.mid_point()[0],
        r.mid_point()[1],
    )
    r = first.get_properties()["rectangle"]
    end = (
        r.mid_point()[0],
        r.mid_point()[1],
    )

    # slowly moves the mouse to the end coordinates
    # this is to prevent the mouse from moving too fast
    # and not dragging the object
    # the farther the distance, the longer it takes
    # to move the mouse
    speed = 50
    if len(args) == 2:
        speed = inter.parse(1, line, args)[2]
        inter.type_err([(speed, (int,))], line, kwargs["lines_ran"])
    # drags the mouse
    movemouse(start, end, speed)
    if p_thread:
        kwargs["auto_lock"].release()
    return True


def f_auto_appelement_drag_coords(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement, movemouse
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret

    r = window.get_properties()["rectangle"]
    start = (
        r.mid_point()[0],
        r.mid_point()[1],
    )
    startcoord = inter.parse(0, line, args)[2]
    endcoord = inter.parse(1, line, args)[2]
    inter.type_err(
        [(startcoord, (int,)), (endcoord, (int,))],
        line,
        kwargs["lines_ran"],
    )
    end = (startcoord, endcoord)
    # gets the speed, if specified
    speed = 50
    if len(args) == 3:
        speed = inter.parse(2, line, args)[2]
        inter.type_err([(speed, (int,))], line, kwargs["lines_ran"])
    # drags the mouse
    movemouse(start, end, speed)
    if p_thread:
        kwargs["auto_lock"].release()
    return True


def f_auto_appelement_backspace(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    window.set_focus()
    # no argument
    if args[0][0] == "":
        ret = window.type_keys("{BACKSPACE}")
    # else, send {BACKSPACE} that many times
    else:
        times = inter.parse(0, line, args)[2]
        inter.type_err([(times, (int,))], line, kwargs["lines_ran"])
        ret = window.type_keys("{BACKSPACE}" * times)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_enter(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = window.type_keys("{ENTER}")
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_hover(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    ret = mouse.move(
        coords=(
            window.get_properties()["rectangle"].mid_point()
        )
    )
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_click(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement, clk
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    waittime = (
        inter.parse(0, line, args)[2] if args[0][0] != "" else 1
    )
    inter.type_err(
        [(waittime, (float, int, complex))], line, kwargs["lines_ran"]
    )
    ret = clk(window, waittime=waittime)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_appelement_right_click(inter, line, args, **kwargs):
    from core.auto.common import _prepare_appelement, clk
    from pywinauto import mouse
    # prepare function
    ret, objfunc, name, window, p_thread, search_queried = _prepare_appelement(
        inter, line, args, **kwargs)
    if search_queried:
        return ret
    waittime = (
        inter.parse(0, line, args)[2] if args[0][0] != "" else 1
    )
    inter.type_err(
        [(waittime, (float, int, complex))], line, kwargs["lines_ran"]
    )
    ret = clk(window, button="right", waittime=waittime)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


OBJ_GENERAL_APPELEMENT_GENERAL_DISPATCH = {
    "window": f_auto_appelement_window,
    "text": f_auto_appelement_text,
    "top": f_auto_appelement_top,
    "bottom": f_auto_appelement_bottom,
    "left": f_auto_appelement_left,
    "right": f_auto_appelement_right,
    "center": f_auto_appelement_center,
    "mid_point": f_auto_appelement_center,
    "rectangle": f_auto_appelement_rectangle,
    "width": f_auto_appelement_width,
    "height": f_auto_appelement_height,
    "element_above": f_auto_appelement_element_above,
    "element_below": f_auto_appelement_element_below,
    "element_left": f_auto_appelement_element_left,
    "element_right": f_auto_appelement_element_right,
    "focus": f_auto_appelement_focus,
    "scroll": f_auto_appelement_scroll,
    "drag": f_auto_appelement_drag,
    "drag_coords": f_auto_appelement_drag_coords,
    "backspace": f_auto_appelement_backspace,
    "enter": f_auto_appelement_enter,
    "hover": f_auto_appelement_hover,
    # extra
    "right_click": f_auto_appelement_right_click,
    **aliases(f_auto_appelement_click, ("click", "left_click"))
}
