
# common
from core.classes.var import Var
from core.common import aliases

def f_sum(inter, line: str, args, **kwargs):
    total = 0
    for i in range(len(args)):
        try:
            total += sum(inter.parse(i, line, args)[2])
        except:
            try:
                total += inter.parse(i, line, args)[2]
            except Exception as e:
                inter.err("Error computing sum", e, line, kwargs["lines_ran"])
    return total

def f_list(inter, line: str, args, **kwargs):
    try:
        return list(inter.parse(0, line, args)[2])
    except:
        return inter.err(
            "Casting error",
            "Could not cast arg to a list",
            line,
            kwargs["lines_ran"],
        )
def f_zip(inter, line: str, args, **kwargs):
    first = inter.parse(0, line, args)[2]
    second = inter.parse(1, line, args)[2]
    # verify both are iterable
    inter.check_iterable(first, line)
    inter.check_iterable(second, line)
    return zip(first, second)
def f_next(inter, line: str, args, **kwargs):
    arg = inter.parse(0, line, args)[2]
    # arg must be iterable
    inter.check_iterable(arg, line)
    return next(arg)
def f_iter(inter, line: str, args, **kwargs):
    arg = inter.parse(0, line, args)[2]
    # arg must be iterable
    inter.check_iterable(arg, line)
    return iter(arg)
def f_len(inter, line: str, args, **kwargs):
    # get the first argument
    arg = inter.parse(0, line, args)[2]
    # arg must be iterable
    inter.check_iterable(arg, line)
    return len(arg)
def f_sortby(inter, line: str, args, **kwargs):
    # iterable to sort
    iterable = inter.parse(0, line, args)[2]
    # iterable must be an iterable
    inter.check_iterable(iterable, line)
    # variable name
    varname = inter.parse(1, line, args)[2]
    # check variable name
    inter.check_varname(varname, line)
    # pairing elements to their interpretations
    pairing = []
    for i in range(len(iterable)):
        inter.vars[varname] = Var(varname, iterable[i])
        pairing.append((inter.interpret(args[2][0]), iterable[i]))
    # sort the pairing based on the first element of each pair
    pairing.sort(key=lambda x: x[0])
    # return the sorted array containing the second element
    # of each pair
    return [pair[1] for pair in pairing]


def f_comp(inter, line: str, args, **kwargs):
    lst = []
    # array to comprehend
    arr = inter.parse(0, line, args)[2]
    # should be an iterable
    inter.check_iterable(arr, line)
    # varname for the element
    varname = inter.parse(1, line, args)[2]
    # should be a varname
    inter.check_varname(varname, line)
    # block to perform
    block = args[2][0]
    # performs the list comprehension
    for v in arr:
        inter.vars[varname] = Var(varname, v)
        r = inter.interpret(block)
        if r != kwargs["msn2_none"]:
            lst.append(r)
    return lst
def f_filter(inter, line: str, args, **kwargs):
    # iterable to filter
    iterable = inter.parse(0, line, args)[2]
    # check if iterable
    inter.check_iterable(iterable, line)
    # variable name
    varname = inter.parse(1, line, args)[2]
    # check variable name
    inter.check_varname(varname, line)
    # new array
    filtered = []
    # iterate through each element
    for v in iterable:
        # set the variable to the element
        inter.vars[varname] = Var(varname, v)
        # if the block returns true, add the element to the new array
        if inter.interpret(args[2][0]):
            filtered.append(v)
    return filtered


def f_unpack(inter, line: str, args, **kwargs):
    # iterable to unpack
    iterable = inter.parse(0, line, args)[2]
    # check if iterable
    inter.check_iterable(iterable, line)
    # variable names to unpack into
    for i in range(1, len(args)):
        varname = inter.parse(i, line, args)[2]
        inter.vars[varname] = Var(varname, iterable[i - 1])
    return iterable


def f_has(inter, line: str, args, **kwargs):
    iterable = inter.parse(0, line, args)[2]
    # iterable must be iterable
    inter.check_iterable(iterable, line)
    # optimized code:
    try:
        return all(
            inter.parse(i + 1, line, args)[2] in iterable
            for i in range(len(args) - 1)
        )
    except Exception as e:
        return inter.err("Error in has()", e, line, kwargs["lines_ran"])
def f_first(inter, line: str, args, **kwargs):
    try:
        return inter.parse(0, line, args)[2][0]
    except:
        return
def f_maximum(inter, line, args, **kwargs):
    try:
        maxval = (
            max(_f)
            if isinstance((_f := inter.parse(0, line, args)[2]), list)
            else _f
        )
        for i in range(1, len(args)):
            val = inter.parse(i, line, args)[2]
            if isinstance(val, list):
                maxval = max(maxval, max(val))
            else:
                maxval = max(maxval, val)
    except Exception as e:
        return inter.err("Error finding maximum value", e, line, kwargs["lines_ran"])
    return maxval
def f_minimum(inter, line, args, **kwargs):
    try:
        minval = (
            min(_f)
            if isinstance((_f := inter.parse(0, line, args)[2]), list)
            else _f
        )
        for i in range(1, len(args)):
            val = inter.parse(i, line, args)[2]
            if isinstance(val, list):
                minval = min(minval, min(val))
            else:
                minval = min(minval, val)
    except Exception as e:
        return inter.err("Error finding minimum value", e, line, kwargs["lines_ran"])
    return minval
def f_op_getarrow(inter, line, args, **kwargs):
    from core.classes.method import Method
    indexable = inter.parse(0, line, args)[2]
    # must be indexable
    if not isinstance(indexable, (list, str, dict, tuple)):
        inter.err(
            "Error indexing with ->()",
            "First argument not indexable, indexable types are lists, strings, dicts, and tuples",
            line,
            kwargs["lines_ran"],
        )
    try:
        return indexable[inter.parse(1, line, args)[2]]
    except IndexError:
        return inter.raise_index_out_of_bounds(
            line, kwargs["lines_ran"], Method("->", inter)
        )
def f_range(inter, line, args, **kwargs):
    start = inter.parse(0, line, args)[2]
    # start must be int
    inter.type_err([(start, (int,))], line, kwargs["lines_ran"])
    # if one argument
    if len(args) == 1:
        return range(start)
    # get the end of the range
    end = inter.parse(1, line, args)[2]
    # end must be int
    inter.type_err([(end, (int,))], line, kwargs["lines_ran"])
    # if two arguments
    if len(args) == 2:
        return range(start, end)
    if len(args) == 3:
        step = inter.parse(2, line, args)[2]
        # step must be int
        inter.type_err([(step, (int,))], line, kwargs["lines_ran"])
        return range(start, end, step)
    return range()
def f_merge(inter, line, args, **kwargs):
    # gets the first argument
    arg1 = inter.parse(0, line, args)[2]
    # arg must exist
    if arg1 is None:
        inter.err(
            "Error in merge()",
            "First argument must exist",
            line,
            kwargs["lines_ran"],
        )
    # gets the rest of the arguments
    for i in range(1, len(args)):
        _arg = inter.parse(i, line, args)[2]
        # arg must exist
        if _arg is None:
            inter.err(
                "Error in merge()",
                "Merging arguments must exist",
                line,
                kwargs["lines_ran"],
            )
        arg1 |= inter.parse(i, line, args)[2]
    return arg1
def f_sorted(inter, line, args, **kwargs):
    iterable = inter.parse(0, line, args)[2]
    # iterable must be iterable
    inter.check_iterable(iterable, line)
    return sorted(iterable)
def f_map(inter, line, args, **kwargs):
    # iterable
    iterable = inter.parse(0, line, args)[2]
    # iterable must be iterable
    inter.check_iterable(iterable, line)
    # varname
    varname = inter.parse(1, line, args)[2]
    # varname must be a varname
    inter.check_varname(varname, line)
    # map the function to each element in the iterable
    for i, el in enumerate(iterable):
        inter.vars[varname] = Var(varname, el)
        iterable[i] = inter.interpret(args[2][0])
    return iterable
def f_insert(inter, line, args, **kwargs):
    # iterable
    iterable = inter.parse(0, line, args)[2]
    # iterable must be iterable
    inter.check_iterable(iterable, line)
    # index
    index = inter.parse(1, line, args)[2]
    # index must be int
    inter.type_err([(index, (int,))], line, kwargs["lines_ran"])
    # value
    value = inter.parse(2, line, args)[2]
    # insert the value into the iterable
    iterable.insert(index, value)
    return iterable

def f_get(inter, line, args, **kwargs):
    iterable = inter.parse(0, line, args)[2]
    # iterable must be iterable
    inter.check_iterable(iterable, line)
    index = inter.parse(1, line, args)[2]
    # index must be int or str
    inter.type_err([(index, (int, str))], line, kwargs["lines_ran"])
    try:
        return iterable[index]
    except IndexError:
        inter.err(
            "Index Error",
            f"Index out of bounds: {index} (you) > {str(len(iterable))} (max)",
            line,
            kwargs["lines_ran"],
        )
def f_getn(inter, line, args, **kwargs):
    # get iterable
    iterable = inter.parse(0, line, args)[2]
    # iterable must be iterable
    inter.check_iterable(iterable, line)
    try:
        # must have at least one index
        ind1 = inter.parse(1, line, args)[2]
        # get at the index
        obj = iterable[ind1]
        # get the rest of the indices
        for i in range(2, len(args)):
            # get the index
            ind = inter.parse(i, line, args)[2]
            # get at the index
            obj = obj[ind]
        return obj
    except:
        inter.err(
            "Error in getn()",
            "Could not index the iterable",
            line,
            kwargs["lines_ran"],
        )
def f_keys(inter, line, args, **kwargs):
    arg = None
    try:
        return (arg := inter.parse(0, line, args)[2]).keys()
    except:
        inter.err(
            "Error getting keys",
            f"Argument must be a dictionary\nYou said: {arg}",
            line,
            kwargs["lines_ran"],
        )
def f_slice(inter, line, args, **kwargs):
    # first
    first = inter.parse(0, line, args)[2]
    # first must be slicable
    inter.check_iterable(first, line)
    # second
    second = inter.parse(1, line, args)[2]
    # second must be int
    inter.type_err([(second, (int,))], line, kwargs["lines_ran"])
    # third
    third = inter.parse(2, line, args)[2]
    # third must be int
    inter.type_err([(third, (int,))], line, kwargs["lines_ran"])
    return first[second:third]
def f_iterablejoin(inter, line, args, **kwargs):
    delimiter = inter.parse(0, line, args)[2]
    # delimiter must be str
    inter.type_err([(delimiter, (str,))], line, kwargs["lines_ran"])
    # iterable
    iterable = inter.parse(1, line, args)[2]
    # iterable must be iterable
    inter.check_iterable(iterable, line)
    return delimiter.join(iterable)
def f_reverse(inter, line, args, **kwargs):
    # arg
    arg = inter.parse(0, line, args)[2]
    # arg must be iterable
    inter.check_iterable(arg, line)
    return arg[::-1]
def f_arr(inter, line: str, args, **kwargs):
    if args[0][0] == "":
        return []
    return [inter.parse(i, line, args)[2] for i in range(len(args))]
def f_object(inter, line: str, args, **kwargs):
    d = {}
    if args[0][0] == "":
        return d
    # cannot have an odd number of arguments
    if len(args) % 2 == 1:
        inter.err(
            "Odd number of arguments in creating object",
            f"An even number of arguments required to have valid key-value pairs.\nYou said: {len(args)} arg(s)",
            line,
            kwargs["lines_ran"],
        )
    # step over arguments in steps of 2
    for i in range(0, len(args), 2):
        d[inter.parse(i, line, args)[2]] = inter.parse(i + 1, line, args)[2]
    return d



ITERABLES_DISPATCH = {
    "sum": f_sum,
    "list": f_list,
    "zip": f_zip,
    "next": f_next,
    "iter": f_iter,    
    "len": f_len,
    "sortby": f_sortby,
    "comp": f_comp,
    "filter": f_filter,
    "unpack": f_unpack,
    "has": f_has,
    "maximum": f_maximum,
    "minimum": f_minimum,
    "->": f_op_getarrow,
    "range": f_range,
    "merge": f_merge,
    "sorted": f_sorted,
    "map": f_map,
    "insert": f_insert,
    "get": f_get,
    "getn": f_getn,
    "keys": f_keys,
    "iterable:join": f_iterablejoin,
    "reverse": f_reverse,
    "slice": f_slice,
    **aliases(f_first, ("first", "head")),
    **aliases(f_arr, ("arr", "from")),
    **aliases(f_object, ("object", "dictfrom")),
}