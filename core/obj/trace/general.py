

def f_trace_this(inter, line: str, args, **kwargs):
    return kwargs["lines_ran"][-1]


def f_trace_before(inter, line: str, args, **kwargs):
    if args[0][0] == "":
        # return all
        return kwargs["lines_ran"]
    numlines = inter.parse(0, line, args)[2]
    # numlines must be int
    inter.type_err([(numlines, (int,))], line, kwargs["lines_ran"])
    return kwargs["lines_ran"][len(kwargs["lines_ran"]) - numlines:]


def f_trace_len(inter, line: str, args, **kwargs):
    return kwargs["total_ints"]



OBJ_TRACE_GENERAL_DISPATCH = {
    "this": f_trace_this,
    "before": f_trace_before,
    "len": f_trace_len,
}