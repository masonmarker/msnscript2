
def f_now(inter, line, args, **kwargs):
    import time
    return time.time()

def f_wait(inter, line, args, **kwargs):
    ret = None
    if len(args) == 1:
        while not (ret := inter.interpret(args[0][0])):
            None
    elif len(args) == 2:
        while not (ret := inter.interpret(args[0][0])):
            inter.interpret(args[1][0])
    elif len(args) == 3:
        import time
        
        s = inter.parse(2, line, args)[2]
        inter.type_err([(s, (int, float))], line, kwargs["lines_ran"])
        while not (ret := inter.interpret(args[0][0])):
            inter.interpret(args[1][0])
            time.sleep(s)
    return ret
def f_interval(inter, line, args, **kwargs):
    import time
    
    # amount of seconds
    seconds = inter.parse(0, line, args)[2]
    # seconds must be int or float
    inter.type_err([(seconds, (int, float))], line, kwargs["lines_ran"])
    # if the interval should last for a certain amount of seconds
    # should account for the first argument to correctly wait
    if len(args) == 3:
        extra = inter.parse(2, line, args)[2]
        # extra must be int or float
        inter.type_err([(extra, (int, float))], line, kwargs["lines_ran"])
        # if time is negative, we set it to infinity
        if extra == -1:
            extra = float("inf")
        end = time.time() + extra
        while time.time() < end:
            time.sleep(seconds)
            inter.interpret(args[1][0])
    else:
        while True:
            time.sleep(seconds)
            inter.interpret(args[1][0])
    return True

def f_sleep(inter, line, args, **kwargs):
    import time

    delay = inter.parse(0, line, args)[2]
    # delay must be int or float
    inter.type_err([(delay, (int, float))], line, kwargs["lines_ran"])
    return time.sleep(delay)

TIME_DISPATCH = {
    "now": f_now,
    "wait": f_wait,
    "interval": f_interval,
    "sleep": f_sleep,
}