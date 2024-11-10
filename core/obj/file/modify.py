

def f_file_create(inter, line, args, **kwargs):
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    open(path, "w").close()
    kwargs["lock"].release()
    return True


def f_file_write(inter, line, args, **kwargs):
    from core.common import file_write
    return file_write(kwargs["inst"], kwargs["lock"], kwargs["lines_ran"])


def f_file_writemsn(inter, line, args, **kwargs):
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    file = open(path, "w")
    towrite = args[1][0]
    file.write(towrite)
    file.close()
    kwargs["lock"].release()
    return towrite


def f_file_clear(inter, line, args, **kwargs):
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    file = open(path, "w")
    file.write("")
    file.close()
    kwargs["lock"].release()
    return True


def f_file_append(inter, line, args, **kwargs):
    from core.common import file_append
    return file_append(kwargs["inst"], kwargs["lock"], kwargs["lines_ran"])


def f_file_delete(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    deleting = inter.parse(0, line, args)[2]
    # deleting must be str
    inter.type_err([(deleting, (str,))], line, kwargs["lines_ran"])
    try:
        os.remove(deleting)
    except:
        None
    kwargs["lock"].release()
    return deleting


def f_file_rename(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    old = inter.parse(0, line, args)[2]
    # old must be str
    inter.type_err([(old, (str,))], line, kwargs["lines_ran"])
    new = inter.parse(1, line, args)[2]
    # new must be str
    inter.type_err([(new, (str,))], line, kwargs["lines_ran"])
    os.rename(old, new)
    kwargs["lock"].release()
    return new


def f_file_copy(inter, line, args, **kwargs):
    import shutil
    kwargs["lock"].acquire()
    old = inter.parse(0, line, args)[2]
    # old must be str
    inter.type_err([(old, (str,))], line, kwargs["lines_ran"])
    new = inter.parse(1, line, args)[2]
    # new must be str
    inter.type_err([(new, (str,))], line, kwargs["lines_ran"])
    shutil.copy2(old, new)
    kwargs["lock"].release()
    return new


def f_file_copy2(inter, line, args, **kwargs):
    import shutil
    kwargs["lock"].acquire()
    old = inter.parse(0, line, args)[2]
    # old must be str
    inter.type_err([(old, (str,))], line, kwargs["lines_ran"])
    new = inter.parse(1, line, args)[2]
    # new must be str
    inter.type_err([(new, (str,))], line, kwargs["lines_ran"])
    shutil.copy2(old, new)
    kwargs["lock"].release()
    return new


def f_file_copyfile(inter, line, args, **kwargs):
    import shutil
    kwargs["lock"].acquire()
    old = inter.parse(0, line, args)[2]
    # old must be str
    inter.type_err([(old, (str,))], line, kwargs["lines_ran"])
    new = inter.parse(1, line, args)[2]
    # new must be str
    inter.type_err([(new, (str,))], line, kwargs["lines_ran"])
    shutil.copyfile(old, new)
    kwargs["lock"].release()
    return new
def f_file_move(inter, line, args, **kwargs):
    import shutil
    kwargs["lock"].acquire()
    old = inter.parse(0, line, args)[2]
    # old must be str
    inter.type_err([(old, (str,))], line, kwargs["lines_ran"])
    new = inter.parse(1, line, args)[2]
    # new must be str
    inter.type_err([(new, (str,))], line, kwargs["lines_ran"])
    shutil.move(old, new)
    kwargs["lock"].release()
    return new


def f_file_mkdir(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    try:
        made = os.mkdir(path)
        kwargs["lock"].release()
        return made
    except FileExistsError:
        kwargs["lock"].release()
        return False
def f_file_rmdir(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    try:
        rm = os.rmdir(path)
        kwargs["lock"].release()
        return rm
    except OSError:
        kwargs["lock"].release()
        return None
def f_file_emptydir(inter, line, args, **kwargs):
    import os
    import shutil
    kwargs["lock"].acquire()
    directory = inter.parse(0, line, args)[2]
    # directory must be str
    inter.type_err([(directory, (str,))], line, kwargs["lines_ran"])
    try:
        for file in os.listdir(directory):
            try:
                os.remove(os.path.join(directory, file))
            except:
                shutil.rmtree(
                    os.path.join(directory, file),
                    ignore_errors=True,
                )
        kwargs["lock"].release()
        return directory
    except FileNotFoundError:
        # directory doesn't exist
        kwargs["lock"].release()
        return None



OBJ_FILE_MODIFY_DISPATCH = {
    "create": f_file_create,
    "write": f_file_write,
    "writemsn": f_file_writemsn,
    "clear": f_file_clear,
    "append": f_file_append,
    "delete": f_file_delete,
    "rename": f_file_rename,
    "copy": f_file_copy,
    "copy2": f_file_copy2,
    "copyfile": f_file_copyfile,
    "move": f_file_move,
    "mkdir": f_file_mkdir,
    "rmdir": f_file_rmdir,
    "emptydir": f_file_emptydir,
}