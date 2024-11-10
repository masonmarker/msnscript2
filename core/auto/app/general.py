

from core.classes.auto.app import App
from core.classes.auto.appelement import AppElement
from core.common import aliases


def f_auto_app_start(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app

    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)

    # determine if a search was initiated
    if search:
        return ret
    
    # create and start the application
    if not kwargs["object"].application:
        from pywinauto.application import Application
        kwargs["object"].application = Application(backend="uia").start(path)
        # add to global apps
        kwargs["apps"][len(kwargs["apps"]) + 1] = inter
        apps = kwargs["apps"]
        ret = kwargs["object"].application

    if p_thread:
        kwargs["auto_lock"].release()

    return ret


def f_auto_app_stop(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app

    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
    
        # determine if a search was initiated
    if search:
        return ret
    # kill the application
    ret = app.kill()
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_print_tree(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # gets the top_window
    ret = app.dump_tree()
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_connection(inter, line, args, **kwargs):
    global apps
    from pywinauto.application import Application
    from core.auto.common import _prepare_app
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # gets a connection to this application
    ret = App(
        kwargs["object"].path,
        Application(backend="uia").connect(
            process=kwargs["object"].application.process
        ),
    )
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_text(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # gets information about this application
    # gets the text of the window
    ret = window.window_text()
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_window(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # gets the window
    ret = window
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_handle(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # gets the handle
    ret = window.handle
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_chrome_children(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # gets the children of this window
    # if not arguments
    if args[0][0] == "":
        ret = window.children()
    # if one argument, check if the first argument is contained
    elif len(args) == 1:
        subtext = inter.parse(0, line, args)[2].lower()
        # subtext must be str
        inter.type_err([(subtext, (str,))], line, kwargs["lines_ran"])
        ret = [
            AppElement(d, d.window_text())
            for d in window.children()
            if subtext in d.window_text().lower()
        ]
    # if two arguments, check if the first argument is exact
    elif len(args) == 2:
        subtext = inter.parse(0, line, args)[2]
        # subtext must be str
        inter.type_err([(subtext, (str,))], line, kwargs["lines_ran"])
        ret = [
            AppElement(d, d.window_text())
            for d in window.children()
            if subtext == d.window_text
        ]

    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_wait_for_text(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app, wait_for_text

    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # if no timeout provided
    if len(args) == 1:
        txt = inter.parse(0, line, args)[2]
        # text should be str
        inter.type_err([(txt, (str,))], line, kwargs["lines_ran"])
        ret = wait_for_text(window, txt)
    # if timeout provided
    elif len(args) == 2:
        txt = inter.parse(0, line, args)[2]
        timeout = inter.parse(1, line, args)[2]
        # text should be str and timeout should be float or int or complex
        inter.type_err(
            [(txt, (str,)), (timeout, (float, int, complex))],
            line,
            kwargs["lines_ran"],
        )
        ret = wait_for_text(window, txt, timeout=timeout)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_wait_for_text_all(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app, wait_for_text_all
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # if no timeout provided
    if len(args) == 1:
        txt = inter.parse(0, line, args)[2]
        # text should be str
        inter.type_err([(txt, (str,))], line, kwargs["lines_ran"])
        ret = wait_for_text_all(window, txt)
    elif len(args) == 2:
        txt = inter.parse(0, line, args)[2]
        timeout = inter.parse(1, line, args)[2]
        # text should be str and timeout should be float or int or complex
        inter.type_err(
            [(txt, (str,)), (timeout, (float, int, complex))],
            line,
            kwargs["lines_ran"],
        )
        ret = wait_for_text_all(window, txt, timeout=timeout)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_wait_for_text_exact(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app, wait_for_text_exact
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # if no timeout provided
    if len(args) == 1:
        txt = inter.parse(0, line, args)[2]
        # text should be str
        inter.type_err([(txt, (str,))], line, kwargs["lines_ran"])
        ret = wait_for_text_exact(window, txt)
    elif len(args) == 2:
        txt = inter.parse(0, line, args)[2]
        timeout = inter.parse(1, line, args)[2]
        # text should be str and timeout should be float or int or complex
        inter.type_err(
            [(txt, (str,)), (timeout, (float, int, complex))],
            line,
            kwargs["lines_ran"],
        )
        ret = wait_for_text_exact(window, txt, timeout=timeout)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_wait_for_text_exact_all(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app, wait_for_text_exact_all
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # if no timeout provided
    if len(args) == 1:
        txt = inter.parse(0, line, args)[2]
        # text should be str
        inter.type_err([(txt, (str,))], line, kwargs["lines_ran"])
        ret = inter.wait_for_text_exact_all(window, txt)
    elif len(args) == 2:
        txt = inter.parse(0, line, args)[2]
        timeout = inter.parse(1, line, args)[2]
        # text should be str and timeout should be float or int or complex
        inter.type_err(
            [(txt, (str,)), (timeout, (float, int, complex))],
            line,
            kwargs["lines_ran"],
        )
        ret = wait_for_text_exact_all(window, txt, timeout=timeout)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_write(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app, convert_keys
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # writes to the window
    writing = inter.parse(0, line, args)[2]
    # writing should be str
    inter.type_err([(writing, (str,))], line, kwargs["lines_ran"])
    try:
        ret = window.type_keys(writing, with_spaces=True)
    except:
        # with_spaces not allowed
        ret = window.type_keys(
            convert_keys(writing), with_spaces=True
        )
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_write_special(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app, convert_keys
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # keystrokes
    keystrokes = inter.parse(0, line, args)[2]
    # keystrokes should be a str
    inter.type_err([(keystrokes, (str,))], line, kwargs["lines_ran"])
    # convert to special characters
    ret = window.type_keys(
        convert_keys(keystrokes), with_spaces=True
    )
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_press(inter, line, args, **kwargs):
    global apps
    from core.auto.common import _prepare_app, press_simul
    # prepare automation function
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    kys = []
    for i in range(len(args)):
        kys.append(inter.parse(i, line, args)[2])
    # presses the keys at the same time
    ret = window.type_keys(press_simul(kys))
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_send_keys(inter, line, args, **kwargs):
    global apps
    import pywinauto
    from core.auto.common import _prepare_app, convert_keys
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
    # determine if a search was initiated
    if search:
        return ret
    keystrokes = inter.parse(0, line, args)[2]
    # keystrokes should be a str
    inter.type_err([(keystrokes, (str,))], line, kwargs["lines_ran"])
    # sends keystrokes to the application
    ret = pywinauto.keyboard.send_keys(
        convert_keys(keystrokes), with_spaces=True
    )
    return ret


def f_auto_app_hovered(inter, line, args, **kwargs):
    import win32api
    from core.auto.common import _prepare_app, get_all

    # prepare
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # get the root window of this application
    root = window.top_level_parent()
    # get the current mouse position
    x, y = win32api.GetCursorPos()
    # recursively find all children from the root window
    # that have the point specified
    ret = get_all(root, x, y)
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_inspect(inter, line, args, **kwargs):
    from core.auto.common import _prepare_app, wait_for_text_all
    # prepare
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # presses the shortcut keys to open the developer tools
    ret = window.type_keys("{F12}")
    # waits for the inspect window to appear
    wait_for_text_all(window, "Console")
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_close_inspect(inter, line, args, **kwargs):
    from core.auto.common import _prepare_app
    # prepare
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # presses the shortcut keys to close the developer tools
    ret = window.type_keys("{F12}")
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_refresh(inter, line, args, **kwargs):
    from core.auto.common import _prepare_app
    # prepare
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # presses the shortcut keys to refresh the page
    ret = window.type_keys("{F5}")
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_enter(inter, line, args, **kwargs):
    from core.auto.common import _prepare_app
    # prepare
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # presses the enter key
    ret = window.type_keys("{ENTER}")
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_escape(inter, line, args, **kwargs):
    from core.auto.common import _prepare_app
    # prepare
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # presses the escape key
    ret = window.type_keys("{ESC}")
    if p_thread:
        kwargs["auto_lock"].release()
    return


def f_auto_app_page_down(inter, line, args, **kwargs):
    from core.auto.common import _prepare_app
    # prepare
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # presses the page down key
    ret = window.type_keys("{PGDN}")
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


def f_auto_app_page_up(inter, line, args, **kwargs):
    from core.auto.common import _prepare_app
    # prepare
    ret, objfunc, path, app, window, search, p_thread = _prepare_app(
        inter, line, args, **kwargs)
        # determine if a search was initiated
    if search:
        return ret
    # presses the page up key
    ret = window.type_keys("{PGUP}")
    if p_thread:
        kwargs["auto_lock"].release()
    return ret


OBJ_GENERAL_APP_DISPATCH = {
    "start": f_auto_app_start,
    "print_tree": f_auto_app_print_tree,
    "connection": f_auto_app_connection,
    "text": f_auto_app_text,
    "window": f_auto_app_window,
    "handle": f_auto_app_handle,
    "chrome_children": f_auto_app_chrome_children,
    "write": f_auto_app_write,
    "write_special": f_auto_app_write_special,
    "press": f_auto_app_press,
    "send_keys": f_auto_app_send_keys,
    "hovered": f_auto_app_hovered,
    "inspect": f_auto_app_inspect,
    "close_inspect": f_auto_app_close_inspect,
    "refresh": f_auto_app_refresh,
    "enter": f_auto_app_enter,
    "escape": f_auto_app_escape,
    "page_down": f_auto_app_page_down,
    "page_up": f_auto_app_page_up,
    **aliases(f_auto_app_wait_for_text, ("wait_text", "wait_for_text")),
    **aliases(f_auto_app_wait_for_text_all, ("wait_text_all", "wait_for_text_all")),
    **aliases(f_auto_app_wait_for_text_exact, ("wait_text_exact", "wait_for_text_exact")),
    **aliases(f_auto_app_wait_for_text_exact_all, ("wait_text_exact_all", "wait_for_text_exact_all")),
    **aliases(f_auto_app_stop, ("stop", "kill", "close"))
}
