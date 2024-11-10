

def f_acquirepointer(inter, line, args, **kwargs):
    return kwargs["pointer_lock"].acquire()


def f_releasepointer(inter, line, args, **kwargs):
    return kwargs["pointer_lock"].release()


POINTER_DISPATCH = {
    "acquire:pointer": f_acquirepointer,
    "release:pointer": f_releasepointer,
}
