"""Common utilities."""

# writes to a file


def file_write(inst, lock, lines_ran):
    lock.acquire()
    path = inst.parse(0)
    # path must be str
    inst.type_err([(path, (str,))], lines_ran)
    file = open(path, "w")
    towrite = str(inst.parse(1))
    file.write(towrite)
    file.close()
    lock.release()
    return towrite

# appends to a file


def file_append(inst, lock, lines_ran):
    lock.acquire()
    path = inst.parse(0)
    # path must be str
    inst.type_err([(path, (str,))], lines_ran)
    file = open(path, "a")
    towrite = str(inst.parse(1))
    file.write(towrite)
    file.close()
    lock.release()
    return towrite


def multi_lined(inst):
    ret = None
    for i in range(len(inst.args)):
        ret = inst.parse(i)
    return ret

# creates aliases for a function name


def aliases(func, aliases):
    return {alias: func for alias in aliases}


def hyphen(inst, **kwargs):
    if len(inst.args) == 1:
        return inst.interpreter.interpret(inst.parse(0),
                                          top_level_inst=kwargs["top_level_inst"])
    # subtracts all arguments from the first argument
    else:
        ret = inst.parse(0)
        try:
            ret = ret.copy()
        except AttributeError:
            pass
        for i in range(1, len(inst.args)):
            ret -= inst.parse(i)
        return ret
