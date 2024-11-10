

from core.common import aliases

def f_pointer_move(inter, line, args, **kwargs):
    from pywinauto import mouse
    return mouse.move(
        coords=(
            inter.parse(0, line, args)[2],
            inter.parse(1, line, args)[2],
        )
    )

def f_pointer_getpos(inter, line, args, **kwargs):
    import win32api
    return win32api.GetCursorPos()

def f_pointer_down(inter, line, args, **kwargs):
    import win32api
    from pywinauto import mouse
    curr_x, curr_y = win32api.GetCursorPos()
    moving = inter.parse(0, line, args)[2]
    # moving must be int
    inter.type_err([(moving, (int,))], line, kwargs["lines_ran"])
    return mouse.move(coords=(curr_x, curr_y + moving))


def f_pointer_up(inter, line, args, **kwargs):
    import win32api
    from pywinauto import mouse
    curr_x, curr_y = win32api.GetCursorPos()
    moving = inter.parse(0, line, args)[2]
    # moving must be int
    inter.type_err([(moving, (int,))], line, kwargs["lines_ran"])
    return mouse.move(coords=(curr_x, curr_y - moving))


def f_pointer_left(inter, line, args, **kwargs):
    import win32api
    from pywinauto import mouse
    curr_x, curr_y = win32api.GetCursorPos()
    moving = inter.parse(0, line, args)[2]
    # moving must be int
    inter.type_err([(moving, (int,))], line, kwargs["lines_ran"])
    return mouse.move(coords=(curr_x - moving, curr_y))


def f_pointer_right(inter, line, args, **kwargs):
    import win32api
    from pywinauto import mouse
    curr_x, curr_y = win32api.GetCursorPos()
    moving = inter.parse(0, line, args)[2]
    # moving must be int
    inter.type_err([(moving, (int,))], line, kwargs["lines_ran"])
    return mouse.move(coords=(curr_x + moving, curr_y))


def f_pointer_drag(inter, line, args, **kwargs):
    import time
    from pywinauto import mouse
    start = (
        inter.parse(0, line, args)[2],
        inter.parse(1, line, args)[2],
    )
    # start[1] and [2] must be int
    inter.type_err(
        [(start[0], (int,)), (start[1], (int,))], line, kwargs["lines_ran"]
    )
    end = (
        inter.parse(2, line, args)[2],
        inter.parse(3, line, args)[2],
    )
    # end[1] and [2] must be int
    inter.type_err(
        [(end[0], (int,)), (end[1], (int,))], line, kwargs["lines_ran"]
    )
    # presses the mouse down at the coordinates
    mouse.press(coords=start)
    # slowly moves the mouse to the end coordinates
    # this is to prevent the mouse from moving too fast
    # and not dragging the object
    # the farther the distance, the longer it takes
    # to move the mouse
    speed = 50
    if len(args) == 5:
        speed = inter.parse(4, line, args)[2]
        # speed must be int
        inter.type_err([(speed, (int,))], line, kwargs["lines_ran"])
    # reverse the speed, so a speed of 50 gives
    # end_range of 50, and a speed of 75 gives
    # end_range of 25
    end_range = 100 - speed
    for i in range(0, end_range):
        mouse.move(
            coords=(
                int(start[0] + (end[0] - start[0]) / 100 * i),
                int(start[1] + (end[1] - start[1]) / 100 * i),
            )
        )
        time.sleep(0.001)
    # releases the mouse at the end coordinates
    mouse.release(coords=end)
    return True





OBJ_POINTER_POSITION_DISPATCH = {
    "down": f_pointer_down,
    "up": f_pointer_up,
    "left": f_pointer_left,
    "right": f_pointer_right,
    "drag": f_pointer_drag,
    **aliases(f_pointer_getpos, ("getpos", "pos", "position")),
    **aliases(f_pointer_move, ("move", "hover")),
}
