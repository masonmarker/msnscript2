


def f_prnt(inter, line, args, **kwargs):
    srep = ""
    for i in range(len(args)):
        srep = str(inter.parse(i, line, args)[2])
        if i != len(args) - 1:
            inter.out += srep + " "
        else:
            inter.out += srep + "\n"
    return srep
def f_print(inter, line, args, **kwargs):
    ret = None
    for i in range(len(args)):
        ret = inter.parse(i, line, args)[2]
        if i != len(args) - 1:
            print(ret, end=" ", flush=True)
        else:
            print(ret, flush=True)
    return ret
def f_printbox(inter, line, args, **kwargs):
    from msnint2 import Interpreter
    ret = None
    for i in range(len(args)):
        ret = inter.parse(i, line, args)[2]
        if i != len(args) - 1:
            print(Interpreter.bordered(str(ret)), end=" ", flush=True)
        else:
            print(Interpreter.bordered(str(ret)), flush=True)
    return ret
def f_printcolor(inter, line, args, **kwargs):
    print_args = [
        inter.parse(i, line, args)[2] for i in range(len(args))
    ]
    return inter.styled_print(print_args)



STDOUT_DISPATCH = {
    "prnt": f_prnt,
    "print": f_print,
    "print:box": f_printbox,
    "print:color": f_printcolor,
}