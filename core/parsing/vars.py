"""Varaible assigning with '=' and associated operators."""


from core.classes.var import Var


def var_assign_or_transform(inter, line):
    line = line[1:]
    element = ""
    variable = ""
    for i in range(0, len(line)):
        c = line[i]
        if c != " ":
            if c == "+" and line[i + 1] == "=":
                variable = element
                element = line[i + 2:]
                # if element is a number
                if isinstance(element, float) or isinstance(element, int):
                    inter.vars[variable].value += inter.interpret(element)
                # if element is a string
                elif isinstance(element, str):
                    try:
                        inter.vars[variable].value += inter.interpret(
                            element)
                    except:
                        inter.vars[variable].value += inter.interpret(
                            element)
                return inter.vars[variable].value
            elif c == "-" and line[i + 1] == "=":
                variable = element
                element = line[i + 2:]
                inter.vars[variable].value -= inter.interpret(element)
                return inter.vars[variable].value
            elif c == "*" and line[i + 1] == "=":
                variable = element
                element = line[i + 2:]
                inter.vars[variable].value *= inter.interpret(element)
                return inter.vars[variable].value
            elif c == "/" and line[i + 1] == "=":
                variable = element
                element = line[i + 2:]
                inter.vars[variable].value /= inter.interpret(element)
                return inter.vars[variable].value
            elif c == "=":
                variable = element
                element = line[i + 1:]
                inter.vars[variable] = Var(
                    variable, inter.interpret(element))
                return inter.vars[variable].value
            else:
                element += c
