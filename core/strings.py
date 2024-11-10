"""Strings functions."""


def f_split(inter, line: str, args, **kwargs):
    first = inter.parse(0, line, args)[2]
    second = inter.parse(1, line, args)[2]
    # first and second must be str
    inter.type_err([(first, (str,)), (second, (str,))],
                   line, kwargs["lines_ran"])
    return inter.parse(0, line, args)[2].split(
        inter.parse(1, line, args)[2]
    )


def f_lines(inter, line: str, args, **kwargs):
    return inter.parse(0, line, args)[2].split("\n")

def f_between(inter, line: str, args, **kwargs):
    # surrounding token
    surrounding = inter.parse(0, line, args)[2]
    # surrounding must be str
    inter.type_err([(surrounding, (str,))], line, kwargs["lines_ran"])
    # string to analyze
    string = inter.parse(1, line, args)[2]
    # string must be str
    inter.type_err([(string, (str,))], line, kwargs["lines_ran"])
    funccalls = []
    try:
        while string.count(surrounding) > 1:
            string = string[
                string.index(surrounding) + len(surrounding):
            ]
            funccalls.append(string[: string.index(surrounding)])
            string = string[
                string.index(surrounding) + len(surrounding):
            ]
    except:
        None
    return funccalls
def f_USD(inter, line, args, **kwargs):
    num = inter.parse(0, line, args)[2]
    # number must be int or float
    inter.type_err([(num, (int, float))], line, kwargs["lines_ran"])
    return f"${num:,.2f}"
def f_format(inter, line, args, **kwargs):
    num = inter.parse(0, line, args)[2]
    # number must be int or float
    inter.type_err([(num, (int, float))], line, kwargs["lines_ran"])
    places = inter.parse(1, line, args)[2]
    # places must be int
    inter.type_err([(places, (int,))], line, kwargs["lines_ran"])
    return f"{num:.{places}f}"
def f_cat(inter, line, args, **kwargs):
    cat = str(inter.parse(0, line, args)[2])
    # concatinate rest of arguments
    for i in range(1, len(args)):
        cat += str(inter.parse(i, line, args)[2])
    return cat

def f_startswith(inter, line, args, **kwargs):
    # arg
    arg = inter.parse(0, line, args)[2]
    # arg must be str
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    # prefix
    prefix = inter.parse(1, line, args)[2]
    # prefix must be str
    inter.type_err([(prefix, (str,))], line, kwargs["lines_ran"])
    return arg.startswith(prefix)
def f_endswith(inter, line, args, **kwargs):
    # arg
    arg = inter.parse(0, line, args)[2]
    # arg must be str
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    # suffix
    suffix = inter.parse(1, line, args)[2]
    # suffix must be str
    inter.type_err([(suffix, (str,))], line, kwargs["lines_ran"])
    return arg.endswith(suffix)
def f_strip(inter, line, args, **kwargs):
    try:
        return inter.parse(0, line, args)[2].strip()
    except Exception as e:
        return inter.err(
            "Error in strip()", e, line, kwargs["lines_ran"]
        )
def f_upper(inter, line, args, **kwargs):
    arg = inter.parse(0, line, args)[2]
    # arg must be str
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    return arg.upper()
def f_lower(inter, line, args, **kwargs):
    arg = inter.parse(0, line, args)[2]
    # arg must be str
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    return arg.lower()
def f_title(inter, line, args, **kwargs):
    arg = inter.parse(0, line, args)[2]
    # arg must be str
    inter.type_err([(arg, (str,))], line, kwargs["lines_ran"])
    # return title
    return arg.title()


STRINGS_DISPATCH = {
    "split": f_split,
    "lines": f_lines,
    "between": f_between,
    "USD": f_USD,
    "format": f_format,
    "cat": f_cat,
    "startswith": f_startswith,
    "endswith": f_endswith,
    "strip": f_strip,
    "upper": f_upper,
    "lower": f_lower,
    "title": f_title,
}