
from core.common import aliases

# replacement insertions
replacements = {
    "<tag>": "#",
    "<nl>": "\n",
    # deep newline
    "<dnl>": "\\n",
    "<rp>": ")",
    "<lp>": "(",
    "<rb>": "]",
    "<lb>": "[",
    "<rcb>": "}",
    "<lcb>": "{",
    "(,)": ",",
    "<or>": "||",
    "< >": " ",
    "<lt>": "<",
    "<gt>": ">",
    "<sq>": "'",
    "<dq>": '"'
}

# other functions


def inter_msn2_replace(inter, script):
    """
    replaces whats in between the tags
    with the interpretation of whats between the tags

    interpretation  is with self.interpret(script)

    script(
        {='hello1'=}

        {=
            cat('hello',
                {='hi there'=}
            )
        =}
    )

    # """
    # do the above but faster and more efficient
    for key in replacements:
        script = script.replace(key, replacements[key])

    def recurse_tags(scr, force_string=False):
        # get the first tag
        # if there is no tag, return the script
        if (first := scr.find(tag)) == -1:
            return scr
        # find the matching end tag
        stack = []
        i = first + len(tag)
        while i < len(scr):
            if scr[i:i + len(endtag)] == endtag:
                if len(stack) == 0:
                    break
                stack.pop()
                i += len(endtag)
            elif scr[i:i + len(tag)] == tag:
                stack.append(tag)
                i += len(tag)
            else:
                i += 1
        # recursively interpret the code between the tags
        interpreted_code = inter.interpret(
            recurse_tags(scr[first + len(tag): i]))
        if force_string:
            interpreted_code = f'"{interpreted_code}"'
        new_scr = f"{scr[:first]}{interpreted_code}{scr[i+len(endtag):]}"
        # recursively continue replacing tags in the remaining script
        return recurse_tags(new_scr)

    # applying '{=' '=}' tags
    tag = "{="
    endtag = "=}"
    with_msn2 = recurse_tags(script)
    return with_msn2


def f_script(inter, line, args, **kwargs):
    # inserts key tokens
    return inter.msn2_replace(args[0][0])


def f_ls(inter, line, args, **kwargs):
    return inter.ls(args)


INSERTIONS_DISPATCH = {
    **aliases(f_script, ("script", "async", "HTML")),
    **aliases(f_ls, ("ls", "longstring")),
}
