

def f_file_read(inter, line, args, **kwargs):
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    file = open(path, "r", encoding="utf-8")
    contents = file.read()
    file.close()
    kwargs["lock"].release()
    return contents
def f_file_fullpath(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    fullpath = os.path.abspath(path)
    kwargs["lock"].release()
    return fullpath


def f_file_exists(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    exists = os.path.exists(path)
    kwargs["lock"].release()
    return exists


def f_file_isdir(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    isdir = os.path.isdir(path)
    kwargs["lock"].release()
    return isdir


def f_file_isfile(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    isfile = os.path.isfile(path)
    kwargs["lock"].release()
    return isfile


def f_file_listdir(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    try:
        listdir = os.listdir(path)
        kwargs["lock"].release()
        return listdir
    except FileNotFoundError:
        # directory doesn't exist
        kwargs["lock"].release()
        return None

def f_file_getcwd(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    cwd = os.getcwd()
    kwargs["lock"].release()
    return cwd

def f_file_getsize(inter, line, args, **kwargs):
    import os
    kwargs["lock"].acquire()
    # get filename
    path = inter.parse(0, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    size = os.path.getsize(path)
    kwargs["lock"].release()
    return size


OBJ_FILE_ACCESS_DISPATCH = {
    "read": f_file_read,
    "exists": f_file_exists,
    "isdir": f_file_isdir,
    "isfile": f_file_isfile,
    "listdir": f_file_listdir,
    "fullpath": f_file_fullpath,
    "getcwd": f_file_getcwd,
    "getsize": f_file_getsize,
}
