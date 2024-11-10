"""Parsing arguments."""

from core.classes.instruction import Instruction


def consume_expression(inter, line, i, l, obj, inst_tree, func, objfunc):
    # newly added, chaining methods
    mergedargs = line[i + 1:l - 1]
    args, chaining_info, _ = get_args(
        inter, mergedargs, func=func, objfunc=objfunc, obj=obj)

    # clean function for handling
    func = func.strip()
    objfunc = objfunc.strip()
    inst = Instruction(line, func, obj, objfunc,
                       args, inst_tree, inter)
    # return pieces of this instruction
    return mergedargs, args, func, objfunc, Instruction(line, func, obj, objfunc,
                                                        args, inst_tree, inter), chaining_info


def consume(inter, line, i, l, obj, inst_tree, func, objfunc):
    return consume_expression(inter, line, i, l, obj, inst_tree, func, objfunc)


def method_args(inter, line, j):
    argstring = ""
    instring = False
    for k in range(j + 1, len(line)):
        if line[k] == '"' and not instring:
            instring = True
        elif line[k] == '"' and instring:
            instring = False
        if not instring:
            if line[k] != " ":
                if line[k] == ")":
                    break
                argstring += line[k]
        else:
            argstring += line[k]
    return argstring.split(","), k


def get_args(inter, line, prev_args=[], chain_index=0,
             prev_line=None, prev_arg=None, chained_int=False,
             func=None, objfunc=None, obj=None, p=0):
    args = []
    l = len(line)
    arg = ""
    start = 0
    p = 0
    a = 0
    s = 0
    indouble = False
    s2 = 0
    insingle = False
    inbacktick = False
    bt = 0
    b = 0
    chain_end = -1
    complete_paren_count = 0
    in_ls = False
    for i in range(l + 1):
        # print(line[:i], in_ls)
        c = ""
        if i < l:
            c = line[i]
        if c == "[" and not s2 > 0 and not s > 0:
            a += 1
        if c == "]" and not s2 > 0 and not s > 0:
            a -= 1
        if c == "(" and not s2 > 0 and not s > 0:
            p += 1
            if func == "ls":
                in_ls = True
                # iterate up to the next ')' to get the arguments
                ls_args = ""
                for k in range(i + 1, l):
                    if line[k] == ")":
                        break
                    ls_args += line[k]
                # add as an arg
                args.append([ls_args, i + 1, i + 1 + len(ls_args)])
                return args, {"is_chained": False}, k
        if c == ")" and not s2 > 0 and not s > 0:
            complete_paren_count += 1
            p -= 1
            if p < 0 and s == 0 and s2 == 0 and a == 0 and b == 0:
                chain_end = None
                # determine if this is chained by iterating through spaces to the first period
                for j in range(i + 1, l):
                    if line[j] != " " and line[j] != ".":
                        break
                    if line[j] == ".":
                        chain_end = j
                        break
                if chain_end:
                    if obj and objfunc:
                        final_line = f"{obj}.{objfunc}({line})"
                    elif func:
                        final_line = f"{func}({line})"
                    else:
                        final_line = f"({line})"
                    a = get_args(
                        inter, final_line, p=p, prev_arg=arg,
                        chain_index=chain_index + 1, func=func, objfunc=objfunc, obj=obj)
                    return a

            # while the next character is a whitespace, skip until there is a period
            if p == 0 and s == 0 and s2 == 0 and a == 0 and b == 0:
                chaining_info = {"is_chained": True,
                                 "start": i + 1, "end": chain_end}
                for j in range(i + 1, l):
                    if line[j] != " " and line[j] != ".":
                        break
                    if line[j] == ".":
                        arg += c
                        # add the arguments from the previous expression
                        args.append([arg, start, start + len(arg)])
                        # recurse for the chained expressions
                        _args, _, end_index = get_args(
                            inter, line[j + 1:], prev_args=args,
                            chain_index=chain_index + 1, prev_line=line,
                            prev_arg=arg, chained_int=True, p=p, func=func, objfunc=objfunc, obj=obj)

                        chaining_info["end"] = end_index
                        chaining_info["p"] = p
                        chaining_info["prev_args"] = prev_args
                        chaining_info["prev_line"] = prev_line
                        chaining_info["prev_arg"] = prev_arg
                        chaining_info["prev_func"] = func
                        chaining_info["prev_objfunc"] = objfunc
                        chaining_info["prev_obj"] = obj

                        args[-1].append(_args)
                        return args, chaining_info, j + chain_index

        if not inter.in_string(s, s2):
            if c == "{":
                b += 1
            if c == "}":
                b -= 1

        if not indouble and not s2 > 0 and c == '"':
            s += 1
            indouble = True
        elif indouble and c == '"':
            s -= 1
            indouble = False

        if not inbacktick and not s2 > 0 and c == "`":
            bt += 1
            inbacktick = True
        elif inbacktick and c == "`":
            bt -= 1
            inbacktick = False

        if not insingle and not s > 0 and c == "'":
            s2 += 1
            insingle = True
        elif insingle and c == "'":
            s2 -= 1
            insingle = False

        if c == "," and s == 0 and s2 == 0 and p == 0 and a == 0 and b == 0:
            args.append([arg, start, start + len(arg)])
            start = i + 1
            arg = ""
            continue
        elif i == l:
            args.append([arg, start, start + len(arg)])
        arg += c
    return args, {"is_chained": False}, -1
