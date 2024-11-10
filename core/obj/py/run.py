

def f_py_run(inter, line: str, args, **kwargs):
    # get the script
    scr = inter.parse(0, line, args)[2]
    # remove all lines starting with '#'
    scr = "\n".join(
        [i for i in scr.split("\n") if not i.startswith("#")]
    )
    # scr must be str
    inter.type_err([(scr, (str,))], line, kwargs["lines_ran"])
    # execute the python and return
    # the snippet with arguments inserted
    return inter.exec_python(scr)

OBJ_PY_RUN_DISPATCH = {
    "run": f_py_run,
}