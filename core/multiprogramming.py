
from core.classes.var import Var


def f_alias(inter, line, args, **kwargs):
    global python_alias
    if args[0][0] == "":
        return python_alias
    new_al = inter.parse(0, line, args)[2]
    # new_al must be str
    inter.type_err([(new_al, (str,))], line, kwargs["lines_ran"])
    python_alias = new_al
    return python_alias
def f_process(inter, line, args, **kwargs):
    import os
    # path to the process to run
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    # if windows:
    if os.name == "nt":
        import subprocess
        # runs the process
        sub = subprocess.run(
            args=[kwargs["python_alias"], "msn2.py", path], shell=True
        )
        inter.processes[path] = sub
        return sub
    # if linux
    elif os.name == "posix":
        inter.err("POSIX not yet implemented", "", line, kwargs["lines_ran"])
        return
    return
def f_proc(inter, line, args, **kwargs):
    # import lib processes module if not imported
    if "lib/processes.msn2" not in inter.imports:
        inter.interpret('import("lib/processes")')
    # import the processes library and
    # create a new process
    name = inter.parse(0, line, args)[2]
    return inter.interpret(
        f"processes:fork('{name}',private(async({args[1][0]})))"
    )
def f_pid(inter, line, args, **kwargs):
    import os
    return os.getpid()
def f_thread(inter, line, args, **kwargs):
    import threading
    global thread_serial
    # name not provided
    if len(args) == 1:
        name = f"__msn2_thread_id_{kwargs['thread_serial']}"
        block = args[0][0]
    # name provided (2 arguments provided)
    else:
        name = str(inter.parse(0, line, args)[2])
        # name must be a varname
        inter.check_varname(name, line)
        block = args[1][0]
    thread = threading.Thread(target=inter.interpret, args=(block,))
    thread.name = name
    inter.threads[name] = [thread, inter]
    thread_serial = kwargs["thread_serial"] + 1
    thread.start()
    return True
def f_threadpool(inter, line, args, **kwargs):
    import concurrent.futures
    
    # get the amount of threads to create
    max_workers = inter.parse(0, line, args)[2]
    # max_workers must be int
    inter.type_err([(max_workers, (int,))], line, kwargs["lines_ran"])
    # create the thread pool
    # submit the block to the pool
    concurrent.futures.ThreadPoolExecutor(max_workers).submit(
        inter.interpret, args[1][0]
    )
    return True
def f_tvar(inter, line, args, **kwargs):
    # thread name
    name = str(inter.parse(0, line, args)[2])
    # variable name
    varname = str(inter.parse(1, line, args)[2])
    # variable value
    val = inter.parse(2, line, args)[2]
    # thread var name
    tvarname = f"_msn2_tvar_{name}_{varname}"
    # sets a thread specific variable
    inter.vars[tvarname] = Var(varname, val)
    return val
def f_gettvar(inter, line, args, **kwargs):
    # gets the variable
    return inter.vars[
        f"_msn2_tvar_{inter.parse(0, line, args)[2]}_{inter.parse(1, line, args)[2]}"
    ].value
def f_tvarstr(inter, line, args, **kwargs):
    # returns the string
    return f"_msn2_tvar_{inter.parse(0, line, args)[2]}_{inter.parse(1, line, args)[2]}"
def f_acquire(inter, line, args, **kwargs):
    return kwargs["auxlock"].acquire()
def f_release(inter, line, args, **kwargs):
    return kwargs["auxlock"].release()
def f_join(inter, line, args, **kwargs):
    for i in range(len(args)):
        name = inter.parse(i, line, args)[2]
        thread = inter.thread_by_name(name)
        while thread is None:
            thread = inter.thread_by_name(name)
        thread.join()
    return True
def f_clearthreads(inter, line, args, **kwargs):
    inter.threads = {}
    return True

MULTIPROGRAMMING_DISPATCH = {
    "alias": f_alias,
    "process": f_process,
    "proc": f_proc,
    "pid": f_pid,
    "thread": f_thread,
    "threadpool": f_threadpool,
    "tvar": f_tvar,
    "gettvar": f_gettvar,
    "tvarstr": f_tvarstr,
    "acquire": f_acquire,
    "release": f_release,
    "join": f_join,
    "clearthreads": f_clearthreads,
}