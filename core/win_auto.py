




from core.classes.auto.app import App


def f_app(inter, line, args, **kwargs):
    import os
    # set timings if not already set
    if not kwargs["timings_set"]:
        from pywinauto import timings

        # pywinauto defaults
        timings.Timings.after_clickinput_wait = 0.001
        timings.Timings.after_setcursorpos_wait = 0.001
        timings.Timings.after_sendkeys_key_wait = 0.001
        timings.Timings.after_menu_wait = 0.001
    # get the path to the application
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    # if there is not second argument, we do not kill any
    # existing instances of the application
    name = None
    extension = None
    if len(args) == 1:
        # get the name and extension of the application
        _sp = path.split("\\")
        name = _sp[-1].split(".")[0]
        extension = _sp[-1].split(".")[1]
        # use taskkill to kill the application
        # taskkill should end the program by name, and should kill
        # all child processes forcefully, it should also not print
        # anything to the console
        os.system(f"taskkill /f /im {name}.{extension} >nul 2>&1")
    # creates an App variable
    return App(path=path, name=name, extension=extension)
def f_connect(inter, line, args, **kwargs):
    from pywinauto.application import Application

    appl = inter.parse(0, line, args)[2]
    a = Application(backend="uia").connect(
        process=appl.application.process
    )
    # connect to the application
    return App(path=appl.path)



WIN_AUTO_DISPATCH = {        
    "app": f_app,
    "connect": f_connect,
}