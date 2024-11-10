

def f_fileacquire(inter, line, args, **kwargs):
    kwargs["lock"].acquire()
    return True


def f_filerelease(inter, line, args, **kwargs):
    kwargs["lock"].release()
    return True


FILE_LOCKS_DISPATCH = {
    "fileacquire": f_fileacquire,
    "filerelease": f_filerelease,
}
