



def f_None(inter, line: str, args, **kwargs):
    return kwargs["msn2_none"]

def f_uuid4(inter, line, args, **kwargs):
    import uuid
    return str(uuid.uuid4())
        
def f_clipboard(inter, line, args, **kwargs):
    import pyperclip
    # if no arguments
    if args[0][0] == "":
        return pyperclip.paste()
    # if one argument
    else:
        copying = str(inter.parse(0, line, args)[2])
        pyperclip.copy(copying)
        return copying
    
MISC_DISPATCH = {
    "None": f_None,
    "uuid4": f_uuid4,
    "clipboard": f_clipboard,
}