"""
Legacy function parsing.

Legacy function declarations are made with the following syntax:
~ func(arg1, arg2) -> return_variable
  -- @return_variable = +(arg1, arg2)


Legacy python fallback is with <<||>> syntax

"""

def legacy_parse_func_body_decl(inter, line):
    line = line[2:]
    try:
        if not inter.methods[inter.loggedmethod[-1]].ended:
            inter.methods[inter.loggedmethod[-1]].add_body(line)
    except:
        None
    return

def legacy_parse_py_fallback(inter, line):
    # parse all text in the line for text surrounded by |
    funccalls = []
    infunc = False
    func = ""
    for i in range(line.rindex(">>")):
        if line[i] == "|" and not infunc:
            infunc = True
        elif line[i] == "|" and infunc:
            infunc = False
            funccalls.append(func)
            func = ""
        elif infunc:
            func += line[i]
    for function in funccalls:
        ret = inter.interpret(function)
        if isinstance(ret, str):
            line = line.replace(f"|{function}|", f'"{str(ret)}"')
        else:
            line = line.replace(f"|{function}|", str(ret))
    line = line[2:-2]
    try:
        return eval(line)
    except:
        return line