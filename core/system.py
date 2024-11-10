

# common
from core.common import aliases



def f_settings(inter, line: str, args, **kwargs):
    return inter.settings
def f_version(inter, line, args, **kwargs):
    return inter.version
def f_parent(inter, line, args, **kwargs):
    return inter.parent
def f_boot(inter, line, args, **kwargs):
    while inter.parent != None:
        inter = inter.parent
    return inter
def f_me(inter, line, args, **kwargs):
    return inter.me()
def f_env(inter, line, args, **kwargs):
    # Build the environment string
    strenv = "--------- environment ---------"
    strenv += f"\nout:\n{inter.out}"
    strenv += "\nvariables:\n"
    for varname, v in inter.vars.items():
        try:
            strenv += f"\t{varname} = {inter.shortened(v.value)}\n"
        except:
            pass
    strenv += "\nmethods:\n"
    for methodname, Method in inter.methods.items():
        strenv += f"\t{methodname}("
        for i in range(len(Method.args)):
            arg = Method.args[i]
            if i != len(Method.args) - 1:
                strenv += f"{arg}, "
            else:
                strenv += str(arg)
        strenv += f") : {len(Method.body)} inst\n"
    
    strenv += "\nmacros:\n\t"
    if len(kwargs["macros"]) > 0:
        strenv += "premacros:\n\t\t"
        for i, macro in enumerate(kwargs["macros"]):
            if i != len(kwargs["macros"]) - 1:
                strenv += f"{macro}\n\t\t"
            else:
                strenv += f"{macro}"
                
    if len(kwargs["postmacros"]) > 0:
        strenv += "\n\tpostmacros:\n\t\t"
        for i, macro in enumerate(kwargs["postmacros"]):
            if i != len(kwargs["postmacros"]) - 1:
                strenv += f"{macro}\n\t\t"
            else:
                strenv += f"{macro}"
    if len(kwargs["syntax"]) > 0:
        strenv += "\n\tsyntax:\n\t\t"
        for i, macro in enumerate(kwargs["syntax"]):
            if i != len(kwargs["syntax"]) - 1:
                strenv += f"{macro}\n\t\t"
            else:
                strenv += f"{macro}"
    if len(kwargs["enclosed"]) > 0:
        strenv += "\n\tenclosedsyntax:\n\t\t"
        for i, macro in enumerate(kwargs["enclosed"]):
            if i != len(kwargs["enclosed"]) - 1:
                strenv += f"{macro}\n\t\t"
            else:
                strenv += f"{macro}"
    strenv += f"\nlog:\n{inter.log}\n-------------------------------"
    
    # If an argument is provided, use styled_print to print with color
    if args[0][0] != "":
        inter.styled_print([
            {"text": "--------- environment ---------", "style": "bold", "fore": "black"},
            {"text": f"\nout:\n{inter.out}", "style": "italic", "fore": "blue"},
            {"text": "\nvariables:", "style": "underline", "fore": "green"},
        ])
        # Print the variables with specific styling (name = value)
        for varname, v in inter.vars.items():
            try:
                inter.styled_print([
                    {"text": f"\t{varname}", "fore": "magenta"},
                    {"text": " = ", "fore": "black"},
                    {"text": f"{inter.shortened(v.value)}", "fore": "yellow"}
                ])
            except:
                None
        # Continue printing other sections with specific styling
        inter.styled_print([
            {"text": "\nmethods:", "style": "underline", "fore": "yellow"}
        ])
        for methodname, Method in inter.methods.items():
            method_pieces = [{"text": f"\t{methodname}(", "fore": "yellow"}]
            for i in range(len(Method.args)):
                arg = Method.args[i]
                method_pieces.append({"text": f"{arg}", "fore": "magenta"})
                if i != len(Method.args) - 1:
                    method_pieces.append({"text": ", ", "fore": "black"})
            method_pieces.append({"text": ")", "fore": "yellow"})
            method_pieces.append({"text": " : ", "fore": "black"})
            method_pieces.append({"text": f"{len(Method.body)} inst", "fore": "black"})
            inter.styled_print(method_pieces)
        
        inter.styled_print([
            {"text": "\nmacros:", "style": "underline", "fore": "red"}
        ])
        if len(kwargs["macros"]) > 0:
            inter.styled_print([{"text": "\tpremacros:", "fore": "red"}])
            for macro in kwargs["macros"]:
                inter.styled_print([{"text": f"\t\t{macro}", "fore": "yellow"}])
        if len(kwargs["postmacros"]) > 0:
            inter.styled_print([{"text": "\tpostmacros:", "fore": "red"}])
            for macro in kwargs["postmacros"]:
                inter.styled_print([{"text": f"\t\t{macro}", "fore": "yellow"}])
        if len(kwargs["syntax"]) > 0:
            inter.styled_print([{"text": "\tsyntax:", "fore": "red"}])
            for macro in kwargs["syntax"]:
                inter.styled_print([{"text": f"\t\t{macro}", "fore": "yellow"}])
        if len(kwargs["enclosed"]) > 0:
            inter.styled_print([{"text": "\tenclosedsyntax:", "fore": "red"}])
            for macro in kwargs["enclosed"]:
                inter.styled_print([{"text": f"\t\t{macro}", "fore": "yellow"}])
        
        inter.styled_print([
            {"text": f"\nlog:\n{inter.log}", "style": "bold", "fore": "black"},
            {"text": "\n-------------------------------", "style": "bold", "fore": "black"}
        ])
    
    # Always return the raw string regardless of printing
    return strenv





def f_envmaxchars(inter, line, args, **kwargs):
    # if no arguments, return the current maxchars
    if args[0][0] == "":
        return inter.env_max_chars
    # otherwise, a single variable was provided
    # this will change the max chars
    new_maxchars = inter.parse(0, line, args)[2]
    # check for type errors
    inter.type_err([(new_maxchars, (int,))], line, kwargs["lines_ran"])
    # alter the max chars
    inter.env_max_chars = new_maxchars
    return new_maxchars
def f_stop(inter, line, args, **kwargs):
    import os
    return os._exit(0)
def f_console(inter, line, args, **kwargs):
    import os
    ret = None
    for i in range(len(args)):
        command = inter.parse(i, line, args)[2]
        # command must be str
        inter.type_err([(command, (str,))], line, kwargs["lines_ran"])
        ret = os.system(command)
    return ret
def f_consoleread(inter, line, args, **kwargs):
    import subprocess

    # returns the console output
    # of the last argument
    command = inter.parse(0, line, args)[2]
    # command must be str
    inter.type_err([(command, (str,))], line, kwargs["lines_ran"])
    process = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    if process.returncode == 0:
        return process.stdout
    else:
        return process.stderr
def f_windows(inter, line, args, **kwargs):
    import os
    return os.name == "nt"
def f_linux(inter, line, args, **kwargs):
    import os
    return os.name == "posix"
def f_mac(inter, line, args, **kwargs):
    import sys
    return sys.platform == "darwin"
def f_exception(inter, line, args, **kwargs):
    # get the error
    error = inter.parse(0, line, args)[2]
    # error must be str
    inter.type_err([(error, (str,))], line, kwargs["lines_ran"])
    # get the message
    message = inter.parse(1, line, args)[2]
    # message must be str
    inter.type_err([(message, (str,))], line, kwargs["lines_ran"])
    # get the line
    l = inter.parse(2, line, args)[2]
    # line must be str
    inter.type_err([(l, (str,))], line, kwargs["lines_ran"])
    # set trying to False
    return inter.err(error, message, l, kwargs["lines_ran"])
def f_import(inter, line, args, **kwargs):
    # for each import
    for i in range(len(args)):
        if script := inter.imp(i, line, args, inter.imports):
            inter.execute(script)
    return

def import_msn2(inter, i, line, args, can_exit, lines_ran):
    path = inter.parse(i, line, args)[2]
    # path must be a string
    inter.type_err([(path, (str,))], line, lines_ran)
    if not path.endswith(".msn2"):
        path += ".msn2"
    if path in can_exit:
        return False
    can_exit.add(path)
    contents = ""
    with open(path) as f:
        contents = f.readlines()
        script = ""
        for line in contents:
            script += line
    inter.logg("importing library", path)
    return script


SYSTEM_DISPATCH = {
    "settings": f_settings,
    "version": f_version,
    "parent": f_parent,
    "boot": f_boot,
    "me": f_me,
    "env": f_env,
    "env:maxchars": f_envmaxchars,
    "stop": f_stop,
    "console": f_console,
    "consoleread": f_consoleread,
    "windows": f_windows,
    "linux": f_linux,
    "mac": f_mac,
    "exception": f_exception,    
    **aliases(f_import, ("import", "launch", "include", "using")),
}