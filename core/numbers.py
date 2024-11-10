

def f_round(inter, line, args, **kwargs):
    num = inter.parse(0, line, args)[2]
    # number must be int or float
    inter.type_err([(num, (int, float))], line, kwargs["lines_ran"])
    digits = inter.parse(1, line, args)[2]
    # digits must be int
    inter.type_err([(digits, (int,))], line, kwargs["lines_ran"])
    return round(num, digits)

def f_random(inter, line, args, **kwargs):
    import random
    # gets a random number between 0 and 1
    if len(args) == 1:
        return random.random()
    # random number in range
    elif len(args) == 2:
        arg = inter.parse(0, line, args)[2]
        # arg must be int
        inter.type_err([(arg, (int,))], line, kwargs["lines_ran"])
        arg2 = inter.parse(1, line, args)[2]
        # arg2 must be int
        inter.type_err([(arg2, (int,))], line, kwargs["lines_ran"])
        return (random.random() * (arg2 - arg)) + arg
    # random int in range
    elif len(args) == 3:
        # using math
        import math
        arg = inter.parse(0, line, args)[2]
        # arg must be int
        inter.type_err([(arg, (int,))], line, kwargs["lines_ran"])
        arg2 = inter.parse(1, line, args)[2]
        # arg must be int
        inter.type_err([(arg2, (int,))], line, kwargs["lines_ran"])
        return math.floor((random.random() * (arg2 - arg)) + arg)
    return "<msnint2 class>"
def f_abs(inter, line: str, args, **kwargs):
    try:
        return abs(inter.parse(0, line, args)[2])
    except:
        return inter.err(
            "Error computing absolute value",
            f"Could not compute absolute value of arg\nConsider changing arg to a number",
            line,
            kwargs["lines_ran"],
        )



NUMBERS_DISPATCH = {
    "round": f_round,
    "random": f_random,
    "abs": f_abs,
}