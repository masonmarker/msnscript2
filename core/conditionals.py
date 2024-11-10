

from core.classes.var import Var

# conditional logic
def f_if(inter, line: str, args, **kwargs):
    # false block is optional
    try:
        false_block_s = args[2][0]
    except:
        false_block_s = None
    ifcond = inter.parse(0, line, args)[2]
    # if condition is true
    if ifcond:
        return inter.parse(1, line, args)[2]
    # otherwise false block is executed
    if false_block_s:
        return inter.parse(2, line, args)[2]
    return False


def f_while(inter, line: str, args, **kwargs):
    while inter.interpret(args[0][0]):
        inter.interpret(args[1][0])
    return True


def f_for(inter, line: str, args, **kwargs):
    # times to loop
    start = inter.parse(0, line, args)[2]
    end = inter.parse(1, line, args)[2]
    loopvar = inter.parse(2, line, args)[2]
    # start must be int
    # end must be int
    # loopvar must be str
    inter.type_err(
        [(start, (int,)), (end, (int,)), (loopvar, (str,))],
        line,
        kwargs["lines_ran"],
    )
    inter.vars[loopvar] = Var(loopvar, start)
    # regular iteration
    if start < end:
        for i in range(start, end):
            if loopvar in inter.vars and inter.vars[loopvar].value >= end:
                break
            inter.vars[loopvar] = Var(loopvar, i)
            inter.interpret(args[3][0])
    # reversed if requested
    elif start > end:
        for i in reversed(range(end, start)):
            if loopvar in inter.vars and inter.vars[loopvar].value < end:
                break
            inter.vars[loopvar] = Var(loopvar, i)
            inter.interpret(args[3][0])
    return inter.vars[loopvar].value


def f_each(inter, line: str, args, **kwargs):
    # get array argument
    array = inter.parse(0, line, args)[2]
    # get element variable name
    element_name = inter.parse(1, line, args)[2]
    # prepare each element
    inter.vars[element_name] = Var(element_name, 0)
    # execute block for each element
    for i in range(len(array)):
        inter.vars[element_name].value = array[i]
        inter.interpret(args[2][0])
    return array

def f_not(inter, line, args, **kwargs):
    return not inter.parse(0, line, args)[2]
def f_and(inter, line, args, **kwargs):
    return all(inter.parse(i, line, args)[2] for i in range(len(args)))
def f_or(inter, line, args, **kwargs):
    return inter.parse(0, line, args)[2] or inter.parse(1, line, args)[2]

def f_break(inter, line, args, **kwargs):
    inter.breaking = True
    return

def _try_compare(inter, func, line, **kwargs):
    try:
        return func()
    except Exception as e:
        return inter.err(
            "Comparison error",
            f"Unable to compare values\n{e}",
            line,
            kwargs["lines_ran"],
        )
def f_greater(inter, line, args, **kwargs):
    return _try_compare(
        inter,
        lambda: inter.parse(0, line, args)[2] > inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )
def f_less(inter, line, args, **kwargs):
    return _try_compare(
        inter,
        lambda: inter.parse(0, line, args)[2] < inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )
def f_greaterequal(inter, line, args, **kwargs):
    return _try_compare(
        inter,
        lambda: inter.parse(0, line, args)[2] >= inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )
def f_lessequal(inter, line, args, **kwargs):
    return _try_compare(
        inter,
        lambda: inter.parse(0, line, args)[2] <= inter.parse(1, line, args)[2],
        line,
        **kwargs,
    )

CONDITIONALS_DISPATCH = {
    "if": f_if,
    "while": f_while,
    "for": f_for,
    "each": f_each,
    "break": f_break,
    "not": f_not,
    "and": f_and,
    "or": f_or,
    "greater": f_greater,
    "less": f_less,
    "greaterequal": f_greaterequal,
    "lessequal": f_lessequal,
}
