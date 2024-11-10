
def f_isstr(inter, line: str, args, **kwargs):
    return isinstance(inter.parse(0, line, args)[2], str)


def f_islist(inter, line: str, args, **kwargs):
    return isinstance(inter.parse(0, line, args)[2], list)


def f_isfloat(inter, line: str, args, **kwargs):
    return isinstance(inter.parse(0, line, args)[2], float)


def f_isint(inter, line: str, args, **kwargs):
    return isinstance(inter.parse(0, line, args)[2], int)


def f_isdict(inter, line: str, args, **kwargs):
    return isinstance(inter.parse(0, line, args)[2], dict)


def f_isinstance(inter, line: str, args, **kwargs):
    return isinstance(
        inter.parse(0, line, args)[2], inter.parse(1, line, args)[2]
    )

def f_isdigit(inter, line, args, **kwargs):
    return inter.parse(0, line, args)[2].isdigit()
def f_isalpha(inter, line, args, **kwargs):
    return inter.parse(0, line, args)[2].isalpha()



TYPE_TESTING_DISPATCH = {
    "isstr": f_isstr,
    "islist": f_islist,
    "isfloat": f_isfloat,
    "isint": f_isint,
    "isdict": f_isdict,
    "isinstance": f_isinstance,
    "isdigit": f_isdigit,
    "isalpha": f_isalpha,
}