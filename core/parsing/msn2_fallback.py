"""
MSN2 Fallback parser.

This insertion style cannot be nested, see functions such as
script() or ls() for recursive parsing.
"""

def macro_msn2_fallback(inter, line):
    # parse all text in the line for text surrounded by %
    funccalls = []
    infunc = False
    func = ""
    for i in range(3, line.rindex("<2>")):
        if line[i] == "%" and not infunc:
            infunc = True
        elif line[i] == "%" and infunc:
            infunc = False
            funccalls.append(func)
            func = ""
        elif infunc:
            func += line[i]

    # for each msn2 evaluation
    for function in funccalls:
        ret = inter.interpret(function)
        if isinstance(ret, str):
            line = line.replace(f"%{function}%", f'"{str(ret)}"')
        else:
            line = line.replace(f"%{function}%", str(ret))
    line = line[3:-3]
    try:
        return inter.interpret(line)
    except:
        try:
            return eval(line, {}, {})
        except:
            return line