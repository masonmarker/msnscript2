# Interpreters MSNScript2
#
# See documentation for more information,
# documentation could lack functions or
# capabilities in this interpreter, as
# this is a work in progress.
#
# docs: masonmarker.com/projects/msn2
# run '{python_alias} msn2cli.py help' for help
#
# Author : Mason Marker
# Start date : 09/15/2022


# _TODO updated 10/16/2024
# TODO
# implement string parsing of the same character at which
# it was defined. ex: "hello \"world\"" -> hello "world"
# currently, this is not possible
#
# TODO
# implement linear interpretation in areas of heavy logic, this applies
# incredibly non linear approaches in several blocks
# such as <<>> or functions such as script()
#
# TODO
# implement warnings and warning handling, as this
# language was designed to be safe yet flexible
#
# TODO
# implement an interpretation for block syntax
# that permits the existence of whitespace / tabs / carriage returns
# in the multilined block to interpret
#
# TODO
# ensure no code repetition
# (it definitely exists)


# the current logical implementation is conceptual,
# deoptimized, and exists to prove functionality as speed can
# be enhanced later, however, opportunities for speed enhancement
# are still being implemented.

# NOTE
# Python runner's alias are determined by
# global python_alias (defined below), defaulting to 'python'
#
# console operations will not run successfully
# if the python runner is incorrect,
# is includes all console() calls, process splitting,
# etc.

# importing necessary dependencies
# for all lines of execution
import os
import json
import warnings
import threading

# classes
from core.classes.instruction import Instruction
from core.classes.var import Var
from core.classes.method import Method
from core.classes.exceptions.msn2exception import MSN2Exception

# parsing
from core.parsing.args import consume, get_args
from core.parsing.legacy.functions import legacy_parse_func_body_decl, legacy_parse_py_fallback
from core.parsing.msn2_fallback import macro_msn2_fallback

# functions
from core.dispatch.functions import FUNCTION_DISPATCH
from core.functions import user_function_exec

# loops
from core.parsing.vars import var_assign_or_transform
from core.special.loops import bar_loop


# remove warnings for calling of integers: "10()"


warnings.filterwarnings("ignore", category=SyntaxWarning)


# path to the common settings file
settings_path = "msn2_settings.json"
# latest version of the interpreter'
# set later
latest_version = None
# if settings does not exist
if not os.path.exists(settings_path):
    # get the latest version number from system/latest.json
    with open("system/latest.json") as f:
        # using the variable declared above
        latest_version = json.load(f)["latest"]
    # create settings
    with open(settings_path, "w") as f:
        # dump default settings
        json.dump(
            {
                "settings": {"has_ran": False, "runner_alias": "python"},
                "version": latest_version,
            },
            f,
        )


# interprets MSNScript2, should create a new interpreter for each execution iteration
# global settings
settings = None
# python alias is in the msn2 settings json
python_alias = "python"
# automation
apps = {}
# obtains the python alias
with open("msn2_settings.json") as f:
    settings = json.load(f)
    python_alias = settings["settings"]["runner_alias"]
# msn2 implementation of None
msn2_none = "___msn2_None_"
# thread serial
thread_serial = 0
# global vars
lock = threading.Lock()
auxlock = threading.Lock()
# lock for pointer controls
pointer_lock = threading.Lock()
# pywinauto automation lock
auto_lock = threading.Lock()
# timings_set switch
timings_set = False
# user defined syntax
syntax = {}
# user defined enclosing syntax
enclosed = {}
# user defined macros
macros = {}
# user defined post macros
# aka macros that are defined that the end of a line
postmacros = {}
# user defined inline syntax
inlines = {}
# OpenAI model presets
# these are the latest models at the time of creation
models = None
# accounting information
inst_tree = {}
lines_ran = []
total_ints = 0
# colors for colored printing,
# defaults to "" until lazily loaded
colors = ""
open_chars = {"(", ",", "{", "[", "=", "{="}


class Interpreter:
    # initializer
    def __init__(self):
        # check if this environment has executed
        # a script before
        if not settings["settings"]["has_ran"]:
            # set has_ran in the json file to true
            settings["settings"]["has_ran"] = True
            # write to the json file
            with open(settings_path, "w") as f:
                import json
                json.dump(settings, f)
        # get the latest version number from system/latest.json
        with open("system/latest.json") as f:
            import json
            global latest_version
            latest_version = json.load(f)["latest"]
        # if the version is not the latest
        if settings["version"] != latest_version:
            # update the version
            settings["version"] = latest_version
            # write to the json file
            with open(settings_path, "w") as f:
                import json
                json.dump(settings, f)
        # set the current settings
        self.settings = settings["settings"]
        # get the version in the json file
        self.version = settings["version"]
        # basic logging
        self.lines = []
        self.out = ""
        self.log = ""
        self.errors = []
        # environment logging
        self.vars = {}
        self.methods = {}
        self.loggedmethod = []
        self.objects = {}
        self.calledmethod = None
        self.env_max_chars = 200
        # advanced environment logging
        self.current_line = 0
        self.breaking = False
        self.breaking_return = []
        self.redirect = None
        self.redirecting = False
        self.redirect_inside = []
        self.imports = set()
        self.domains = set()
        # threading
        self.thread = None
        self.threads = {}
        self.parent = None
        # ChatGPT connections
        self.openaikey = None
        self.tokens = 100
        self.browser_path = None
        self.serial_1 = 0
        # hosting endpoints
        self.endpoints = {}
        self.endpoint_datas = {}
        self.endpoint_path = "demos/practical/apidata/apitestdata.csv"
        # multiprocessing
        self.processes = {}
        # global and local scopes for internal Python environment
        self._globals = {}
        self._locals = {}
        # in a try block
        self.trying = False
        # web
        # converting JavaScript?
        self.using_js = False
        # web imports
        self.web_imports = set()
        # states
        self.states = {}
        # routes
        self.routes = {}
        # NextJS generation
        self.next_entry_path = None
        self.next_project_path = None

    # determines if a line is a comment or not

    def is_comment(self, _line):
        return _line.startswith("#") or _line.startswith("::")

    # executes stored script
    def execute(self, script, include_temp_vars=True):
        # convert script to lines
        self.lines = []
        # for aggregate syntax support !{}
        inml = False
        ml = ""
        # for block syntax
        inblock = False
        p = 0
        # whether or not to keep
        keep_space = False
        keep_block = ""
        skipping = False
        # for each line of code
        for line in script.split("\n"):
            # add to list of liness
            self.lines.append(line)
            # continue if this line is a comment
            if self.is_comment(line):
                continue
            # for running Python
            if not keep_space and line.endswith("\\\\"):
                # determine if this script should run
                # based on the expression at the beginning of the line
                line = line[:-2]
                line = line.strip()
                # if there is a conditional Python execution
                if line:
                    # execute the conditional line
                    # with import capabilities
                    result = self.interpret(line,
                                            top_level_inst=True, has_outer_function=False,
                                            include_temp_vars=include_temp_vars)
                    keep_space = True
                    # if the conditional evaluated to True
                    if result:
                        # if the conditional line is true, then execute the Python
                        skipping = False
                        keep_block = ""
                    # otherwise, skip the Python
                    else:
                        skipping = True
                        keep_block = ""
                else:
                    skipping = False
                    keep_space = True
                    keep_block = ""
            # if the Python block has been ended
            elif keep_space and line.endswith("\\\\"):
                # if skipping
                if skipping:
                    skipping = False
                    keep_block = ""
                    keep_space = False
                    continue
                # fix line
                line = line[:-2]
                line = line.strip()
                # remove the trailing newline
                # character
                keep_block = keep_block[:-1]
                # modify conditionals
                keep_space = False
                # if setting to a variable
                if line:
                    # set variable to python block
                    self.vars[line] = Var(line, keep_block)
                else:
                    # execute Python
                    self.exec_python(
                        keep_block, has_outer_function=False, include_temp_vars=include_temp_vars)
                # reset python block and skipping flag
                keep_block = ""
                skipping = False
            # skipping this Python block
            # due to conditional
            elif keep_space and skipping:
                continue
            # if in a python block
            elif keep_space:
                keep_block += f"{line}\n"
                self.current_line += 1
                continue
            else:
                line = line.strip()
            if self.is_comment(line):
                self.current_line += 1
                continue
            else:
                # aggregate syntax !{} (not recommended for most cases)
                if line.startswith("!{") and line.endswith("}"):
                    ml = line[2:-1]
                    self.interpret(ml, top_level_inst=True,
                                   has_outer_function=False)
                    ml = ""
                elif not inml and line.startswith("!{"):
                    inml = True
                    ml += line[2:]
                elif inml and line.endswith("}"):
                    inml = False
                    ml += line[0: len(line) - 1]
                    self.interpret(ml, top_level_inst=True,
                                   has_outer_function=False, include_temp_vars=include_temp_vars)
                    ml = ""
                elif inml:
                    ml += line
                # block syntax (recommended for most cases)
                elif not inblock and any(line.endswith(char) for char in open_chars):
                    for c in line:
                        if c == "(":
                            p += 1
                        if c == ")":
                            p -= 1
                        ml += c
                    inblock = True
                elif inblock:
                    for i in range(len(line)):
                        c = line[i]
                        if c == "(":
                            p += 1
                        if c == ")":
                            p -= 1
                        # end of syntax met
                        if p == 0:
                            ml += line[i:]
                            inter = ml
                            ml = ""
                            inblock = False
                            self.interpret(
                                inter, keep_space=keep_space, top_level_inst=True,
                                has_outer_function=False, include_temp_vars=include_temp_vars)
                            break
                        ml += c
                else:
                    self.interpret(line, keep_space=keep_space,
                                   top_level_inst=True, has_outer_function=False,
                                   include_temp_vars=include_temp_vars)
            self.current_line += 1
        return self.out

    def replace_vars(self, line):
        boo = line
        for varname in sorted(self.vars.keys(), key=len, reverse=True):
            try:
                boo = boo.replace(
                    varname, str(self.get_var(eval(f'"{varname}"', {}, {})))
                )
            except:
                None
        return boo

    # function to attempt to pull an integer out of the function
    # if it is an integer, then it is a loop that runs func times
    def get_int(self, func):
        try:
            return int(func)
        except:
            return None

    def interpret(self, line, block={},
                  keep_space=False, is_chained=False,
                  top_level_inst=False, has_outer_function=True,
                  include_temp_vars=True):

        # acquiring globals
        global total_ints, lock, lines_ran, auxlock, \
            auto_lock, pointer_lock, python_alias, inst_tree

        # accounting
        total_ints += 1
        lines_ran.append(line)
        # determine the location of this instruction
        # in the inst_tree depending on lines_ran
        # and the current line
        inst_tree[total_ints] = [self.current_line, line]
        # interpreter is breaking
        if self.breaking:
            return self.breaking_return
        # strip line for interpretation
        if not keep_space and hasattr(line, 'strip'):
            line = line.strip()
        else:
            return
        l = len(line)
        # whether the line should immediately continue or not
        cont = False

        if not line:
            return

        # the below conditions interpret a line based on initial appearances
        # beneath these conditions will the Interpreter then parse the arguments from the line as a method call

        # method-specific line reached
        if line.startswith("--"):
            return legacy_parse_func_body_decl(self, line)
        # new variable setting and modification syntax as of 12/20/2022
        # iterates to the first '=' sign, capturing the variable name in the
        # process (as it should)
        if line[0] == "@":
            return var_assign_or_transform(self, line)

        # determine if we're using JS
        if line.startswith("JS:"):
            self.using_js = True
            return self.using_js
        if line.endswith(":JS"):
            self.using_js = False
            return self.using_js

        # python fallback mode specification,
        # both <<>> and
        if line.startswith("<<"):
            return legacy_parse_py_fallback(self, line)

        # embedded MSN2 interpretation macro
        if line.startswith("<2>"):
            return macro_msn2_fallback(self, line)

        # user defined syntax
        for key in syntax:
            if line.startswith(key):
                return self.run_syntax(key, line, has_outer_function=has_outer_function)
        # user defined macro
        for token in macros:
            if line.startswith(token):
                # if the macro returns a value instead of executing a function
                if len(macros[token]) == 4:
                    return macros[token][3]
                # variable name
                varname = macros[token][1]
                val = line[len(token):]
                # store extended for user defined syntax
                self.vars[varname] = Var(varname, val)
                # execute function
                return self.interpret(macros[token][2], top_level_inst=top_level_inst, has_outer_function=False)
        # user defined postmacro
        for token in postmacros:
            if line.endswith(token):
                # if the macro returns a value instead of executing a function
                if len(postmacros[token]) == 4:
                    return postmacros[token][3]
                varname = postmacros[token][1]
                val = line[0: len(line) - len(token)]
                self.vars[varname] = Var(varname, val)
                return self.interpret(postmacros[token][2], top_level_inst=top_level_inst, has_outer_function=False)

        # variable replacement, generally unsafe, but replaces
        # all variable names as they're written the the expression after
        # the '*'
        if line[0] == "*":
            return self.interpret(self.replace_vars(line[1:]))

        # invoking user defined enclosing syntax
        for key in enclosed:
            start = enclosed[key][0]
            end = enclosed[key][1]
            if line.startswith(start) and line.endswith(end):
                if len(enclosed[key]) == 5:
                    return enclosed[key][4]
                varname = enclosed[key][2]
                self.vars[varname] = Var(
                    varname, line[len(start): len(line) - len(end)]
                )
                return self.interpret(enclosed[key][3], has_outer_function=False)

        # checks for active Interpreter redirect request
        # generally slow, due to checking for the redirect
        if self.redirecting and not "stopredirect()" in line.replace(" ", ""):
            self.redirect_inside.append([self.redirect[1], line])
            return self.redirect

        # try base literal
        try:
            if not line.startswith("--"):
                # try evaluating the line
                _ret = eval(line, {}, {})
                # eval cannot be a python class, because names of variables
                # could result in python classes
                # should also not be a built in function
                if not isinstance(_ret, type) and not isinstance(_ret, type(eval)):
                    return _ret
        except:
            pass

        # 2.0.403
        # iterate through the line to determine if we're chaining
        # deoptimized approach, implemented for functionality
        a = get_args(self, line)[0]
        if len(a) == 1 and len(a[0]) == 4:
            new_args, take_return = self.get_new_args(a)
            if take_return:
                return new_args
            return self.interpret(new_args[0][0])

        func = ""
        objfunc = ""
        obj = ""
        s = 0
        sp = 0
        for i in range(l):
            if cont:
                continue
            if i < len(line):
                c = line[i]
            else:
                break
            if c == " " and s == 0:
                sp += 1
                continue
            if c == ".":
                obj = func
                func = ""
                objfunc = ""
                continue
            # legacy method declaration, not recommended for use,
            # but kept for backwards compatibility
            if c == "~":
                return self.legacy_curly_func_decl(line, i)

            # interpreting a function
            elif c == "(":
                # consuming
                mergedargs, args, func, objfunc, inst, chaining_info = consume(
                    self, line, i, l, obj, inst_tree, func, objfunc)

                # 2.0.403
                # basic method chaining
                if chaining_info["is_chained"]:
                    args, take_return = self.get_new_args(args)
                    if take_return:
                        return args
                    return self.interpret_expression(
                        Instruction(line, func, obj, objfunc,
                                    args, inst_tree, self),
                        args, obj, objfunc, line, func, line,
                        is_chained=True, top_level_inst=top_level_inst
                    )
                # standard interpretation
                return self.interpret_expression(inst, args, obj,
                                                 objfunc, mergedargs, func, line,
                                                 top_level_inst=top_level_inst)
            if obj != "":
                objfunc += c
            else:
                func += c
        # try a variable
        if line in self.vars:
            return self.vars[line].value
        # otherwise nothing
        # try replacing variables 2
        try:
            line = self.replace_vars2(line)
        except:
            pass
        # get value of line
        try:
            return eval(line, {}, {})
        except:
            try:
                return eval(str(self.replace_vars(line)), {}, {})
            except:
                return

    def legacy_curly_func_decl(self, line, i):
        returnvariable = ""
        self.loggedmethod.append("")
        for j in range(i + 1, len(line)):
            if line[j] != " ":
                if line[j] == "(":
                    args = self.method_args(line, j)
                    for k in range(args[1], len(line)):
                        if line[k] != " ":
                            if line[k] == "-" and line[k + 1] == ">":
                                for l in range(k + 2, len(line)):
                                    if line[l] != " ":
                                        returnvariable += line[l]
                    break
                self.loggedmethod[-1] += line[j]
        if self.loggedmethod[-1] not in self.methods.keys():
            self.methods[self.loggedmethod[-1]] = Method(
                self.loggedmethod[-1], self
            )
        else:
            # break out of the loop that called this function
            return
        for arg in args[0]:
            if arg != "":
                self.vars[arg] = None
                self.methods[self.loggedmethod[-1]].add_arg(arg)
        self.methods[self.loggedmethod[-1]].add_return(returnvariable)
        return self.loggedmethod[-1]

    def get_new_args(self, new_args):
        _gotten_new_args = self._get_new_args(new_args)
        _new_gotten_new_args = []
        for argset in _gotten_new_args:
            if argset[0].strip().startswith("@"):
                new_line = ""

                def recurse(argset):
                    nonlocal new_line
                    new_line += f"{argset[0]}."
                    if len(argset) == 3:
                        new_line = new_line[:-1]
                        return
                    elif len(argset) == 4:
                        recurse(argset[3])
                recurse(argset)
                _new_gotten_new_args.append([new_line, 0, 0])
            else:
                _new_gotten_new_args.append(argset)
        _gotten_new_args = _new_gotten_new_args

        _new_args = []
        for exp in _gotten_new_args:
            if len(exp) == 4:
                adding = self._interpret_chain(exp)
                _new_args.append(adding)
            else:
                _new_args.append(exp)
        return _new_args, False

    def _get_new_args(self, args):
        def process_list(lst):
            result = []
            promoted = []
            first = True
            for elem in lst:
                if isinstance(elem, list):
                    if len(elem) >= 4 and isinstance(elem[3], list):
                        processed_chain, chain_promoted = process_list(
                            elem[3])
                        if len(processed_chain) == 1:
                            elem[3] = processed_chain[0]
                        else:
                            elem[3] = processed_chain
                        if first:
                            result.append(elem)
                            first = False
                        else:
                            promoted.append(elem)
                        promoted.extend(chain_promoted)
                    else:
                        if first:
                            result.append(elem)
                            first = False
                        else:
                            promoted.append(elem)
                else:
                    result.append(elem)
            return result, promoted
        processed_args, promoted_args = process_list(args)
        return processed_args + promoted_args

    def _interpret_chain(self, chain_exp, vn=None, i=0, chain_line=""):
        if len(chain_exp) == 3:
            # if chain_line ends in a ',', remove it
            if chain_line.endswith(","):
                chain_line = chain_line[:-1]
            # based on func, obj and objfunc, create the final instruction
            return [f"{chain_line},var('{vn}',{vn}.{chain_exp[0]},True),{vn})", 0, 0]

        # interpret this expression
        if i == 0:
            # create a temporary variable for chaining
            temp = self.temp_safe_var()
            # initial line
            init_line = f"(var('{temp.name}',{chain_exp[0]},True),"
            return self._interpret_chain(chain_exp[-1], temp.name, i + 1, init_line)
        else:
            # otherwise, we're doing a chain interpretation
            # get the variable name
            final_line = f"var('{vn}',{vn}.{chain_exp[0]},True),"
            # interpret the expression
            return self._interpret_chain(chain_exp[-1], vn, i + 1, chain_line + final_line)

    def temp_safe_var(self):
        import random
        from core.classes.var import RESERVED_VARNAME_PREFIX
        name = ""
        while name == "" or name in self.vars:
            name = f"{RESERVED_VARNAME_PREFIX}_temp{random.randint(0, 9999999)}"
        return Var(name, None, force_allow_name=True)

    # interprets an expression

    def interpret_expression(self, inst, args, obj, objfunc,
                             mergedargs, func, line, is_chained=False,
                             top_level_inst=False, has_outer_function=True):

        # if using_js
        if self.using_js:
            return inst.convert_to_js(lock, lines_ran)

        # class attribute / method access
        if obj in self.vars:
            vname = obj
            object = getattr(self.vars.get(
                obj), 'value', self.vars.get(obj))

            _type_object = type(object)
            try:
                # if the object is a class
                if objfunc in object:
                    # if the object is a Method
                    if isinstance(object[objfunc], Method):
                        # get the Method object
                        method = object[objfunc]
                        # get the number of arguments to the method
                        num_args = len(method.args)
                        # args to pass to the function
                        to_pass = [vname]
                        # if there is no argument
                        if args[0][0] != "":
                            # for each parsed argument
                            for k in range(num_args):
                                try:
                                    to_pass.append(
                                        self.parse(k, line, args)[2])
                                except:
                                    pass
                        # create return variable
                        ret_name = method.returns[0]
                        # if the return variable doesn't exist
                        if ret_name not in self.vars:
                            self.vars[ret_name] = Var(ret_name, None)
                        # insert vname into args[0]
                        args.insert(0, [vname])
                        # execute method
                        try:
                            method.run(to_pass, self, args)
                        # Index out of bounds error
                        except IndexError:
                            self.raise_incorrect_args(
                                str(len(method.args)),
                                str(self.arg_count(args) - 1),
                                line,
                                lines_ran,
                                method,
                            )
                        try:
                            return eval(
                                str(self.vars[method.returns[0]].value), {
                                }, {}
                            )
                        except:
                            try:
                                return str(self.vars[method.returns[0]].value)
                            except:
                                return str(self.vars[method.returns[0]])
                    # otherwise if we're accessing an attribute
                    # no arguments given
                    if args[0][0] == "":
                        return object[objfunc]
                    # parameter provided, wants to set attribute
                    param = self.parse(0, line, args)[2]
                    self.vars[obj].value[objfunc] = param
                    return param
            except MSN2Exception as e:
                raise e
            except:
                pass
            # # as of 2.0.388,
            # # if the objfunc ends with '!',
            # # it becomes destructive
            # # and returns the object
            if objfunc.endswith("!"):
                return FUNCTION_DISPATCH["obj"]["general"]["!"](
                    self, line, args, vname=vname, objfunc=objfunc, mergedargs=mergedargs
                )
            if objfunc in FUNCTION_DISPATCH["obj"]["general"]["default"]:
                return FUNCTION_DISPATCH["obj"]["general"]["default"][objfunc](
                    self, line, args, vname=vname, objfunc=objfunc, mergedargs=mergedargs,
                    object=object, obj=obj, lines_ran=lines_ran
                )

            # variable type specific methods

            # do the above but without code repetition
            # check for general functions
            if _type_object in FUNCTION_DISPATCH["obj"]["general"]:
                if objfunc in FUNCTION_DISPATCH["obj"]["general"][_type_object]:
                    return FUNCTION_DISPATCH["obj"]["general"][_type_object][objfunc](
                        self, line, args, vname=vname, objfunc=objfunc,
                        object=object, obj=obj, lines_ran=lines_ran, apps=apps, inst_tree=inst_tree
                    )

            # check for requests_html.HTML
            elif str(_type_object) in FUNCTION_DISPATCH["obj"]["general"]["class_based"]:
                if objfunc in FUNCTION_DISPATCH["obj"]["general"]["class_based"][_type_object]:
                    return FUNCTION_DISPATCH["obj"]["general"]["class_based"][_type_object][objfunc](
                        self, line, args, object=object, objfunc=objfunc
                    )
                else:
                    return FUNCTION_DISPATCH["obj"]["general"]["class_based"][_type_object]["else"](
                        self, line, args, object=object, objfunc=objfunc
                    )
        # user function execution requested
        # user functions take priority
        # over general msn2 functions
        if func in self.methods:
            return user_function_exec(inst, lines_ran)

        # the  belowconditions interpret a line based on initial appearances
        # beneath these conditions will the Interpreter then parse the arguments from the line as a method call
        # request for Interpreter redirect to a block of code
        elif func in FUNCTION_DISPATCH:
            return FUNCTION_DISPATCH[func](
                self, line, args,
                inst=inst, lines_ran=lines_ran, total_ints=total_ints, msn2_none=msn2_none,
                macros=macros, postmacros=postmacros, enclosed=enclosed, syntax=syntax, python_alias=python_alias,
                auxlock=auxlock, pointer_lock=pointer_lock, timings_set=timings_set, thread_serial=thread_serial,
                is_chained=is_chained, top_level_inst=top_level_inst, has_outer_function=has_outer_function
            )

        # for objects
        elif obj in FUNCTION_DISPATCH["obj"]:
            if objfunc in FUNCTION_DISPATCH["obj"][obj]:
                return FUNCTION_DISPATCH["obj"][obj][objfunc](
                    self, line, args,
                    inst=inst, lines_ran=lines_ran, total_ints=total_ints, lock=lock
                )
            else:
                return FUNCTION_DISPATCH["obj"][obj]["else"](
                    self, line, args,
                    inst=inst, lines_ran=lines_ran, total_ints=total_ints, objfunc=objfunc
                )

        # # object instance requested
        # # if the function is in the variables
        # # and the variable is a class
        elif func in self.vars and isinstance(self.vars[func].value, dict):
            return FUNCTION_DISPATCH["obj"]["instance"]["new"](
                self, line, args, func=func
            )

        # quicker conditional operator as functional prefix
        elif len(func) > 0 and func[0] == "?":
            return FUNCTION_DISPATCH["special"]["?"](
                self, line, args, func=func
            )

        # inline function, takes any amount of instructions
        # returns the result of the last instruction
        elif func == "" and objfunc == "":
            return FUNCTION_DISPATCH["=>"](self, line, args, inst=inst)
        # if the function, when parsed, is an integer,
        # then it is a loop that runs func times
        elif (_i := self.get_int(func)) is not None:
            return FUNCTION_DISPATCH["special"]["intloop"](
                self, line, args, _i=_i
            )

        # if the function is a variable name
        elif func in self.vars:
            return FUNCTION_DISPATCH["special"]["varloop"](
                self, line, args, func=func
            )

        # functional syntax for easier to write loops
        # cannot receive non literal or variable arguments, or any expression containing a '|'
        # syntax:     3|5|i (prnt(i))
        # prnts 3\n4\n5
        # Functional syntax for loops like 3|5|i (prnt(i))
        # elif func.count("|") == 2:
        elif (_func_split := func.split("|")) and len(_func_split) == 3:
            return bar_loop(self, line, args, _func_split=_func_split)
        # fallback
        else:
            try:
                line = self.replace_vars2(line)
                return eval(line, {}, {})
            except:
                # maybe its a variable?
                try:
                    return self.vars[line].value
                except:
                    # ok hopefully its a string lol
                    return line

    # adds a new program wide syntax

    def add_syntax(self, token, between, function):
        syntax[token] = [between, function]
        return [token, between, function]

    # exporting error messages
    def export_err(self, vname, line):
        if vname not in self.vars:
            return self.err(
                f"Error exporting variable",
                f'Variable "{vname}" does not exist in this context.',
                line,
                lines_ran,
            )

    # class specific error messages
    def no_var_err(self, _vn, _type, _and, _locals, line):
        return self.err(
            f'No {_type} variable "{_vn}" found in Python environment',
            f'Current {_and} environment locals:\n{self._locals}\nsize: {len(self._locals)}\nsee globals with "py.globals()"',
            line,
            lines_ran,
        )

    # ls: long string
    def ls(self, args):
        # print(args)
        return self.msn2_replace(",".join([str(arg[0]) for arg in args]).strip())

    # replaces tokens in the string with certain
    # characters or values
    # TODO: implement linear interpretation

    def msn2_replace(self, script):
        from core.insertions import inter_msn2_replace
        return inter_msn2_replace(self, script)

    # determines the number of arguments based on the args array
    def arg_count(self, args):
        # no arguments supplied
        if args[0][0] == "":
            return 0
        else:
            return len(args)

    # returns True if should go to the next file to import
    def imp(self, i, line, args, can_exit):
        from core.system import import_msn2
        return import_msn2(self, i, line, args, can_exit, lines_ran)

    # creates a child interpreter
    def new_int(self):
        ret = Interpreter()
        ret.parent = self
        ret.trying = self.trying
        return ret

    def run_syntax(self, key, line, has_outer_function=True):
        # get everything between after syntax and before next index of syntax
        # or end of line
        inside = line[len(key): line.rindex(key)]
        invarname = syntax[key][0]
        function = syntax[key][1]
        self.vars[invarname] = Var(invarname, inside)
        return self.interpret(function, has_outer_function=has_outer_function)

    def replace_vars2(self, line):
        for varname, var in self.vars.items():
            try:
                val = var.value
            except:
                try:
                    val = eval(str(var), {}, {})
                except:
                    val = str(var)
            if isinstance(val, str):
                val = f'"{val}"'
            line = line.replace(f"?{varname}?", str(val))
        return line

    # gets a thread by name

    def thread_by_name(self, name):
        try:
            # thread exists
            return self.env_by_name(name)[0]
        except:
            # thread does not exist (yet)
            return

    # gets an environment by name

    def env_by_name(self, name):
        try:
            return self.threads[name]
        except KeyError:
            return

    # splits a named argument in a function

    def split_named_arg(self, as_s, method, func_args, user_func=False):
        # name of argument
        meth_argname = ""
        # iterate up to the first '=' in as_s
        for j in range(1, len(as_s)):
            if as_s[j] == "=":
                last_ind = j + 1
                break
            # cannot be space
            if as_s[j] != " ":
                meth_argname += as_s[j]
        # argument to interpret
        arg = as_s[last_ind:]
        # set the method arg at the specified index
        # to the corresponding argument name in method.args
        # similar to that of Python's argument picker func(arg1=None, arg2=None)
        # get the index of the named argument in method.args
        try:
            ind = method.args.index(meth_argname)
        except ValueError:
            # if not user_func:
            # find the argument
            method.args.append(meth_argname)
            ind = method.args.index(meth_argname)
            # else:

        # adjust the func_args list to the correct size
        if len(func_args) < ind + 1:
            func_args += [None] * (ind + 1 - len(func_args))
        # print(func_args, ind)
        # set the argument at the index to the value
        func_args[ind] = self.interpret(arg)
        return func_args, meth_argname, arg, ind

    # parses an argument from a function
    def parse(self, arg_number, line, args, top_level_inst=False):
        return line, (as_s := args[arg_number][0]), self.interpret(as_s, top_level_inst)

    # gets the shortened version of a variable's value
    def shortened(self, needs_short):
        # if the string is greater than 200 chars
        if len(_t := str(needs_short)) > self.env_max_chars:
            return f"{_t[:self.env_max_chars]}..."
        # otherwise, return the string
        return _t

    # starts a user shell

    def shell(self):
        ip = None
        while ip != "exit":
            ip = input(">>> ")
            self.interpret(ip)

    # logs something to the console

    def logg(self, msg, line):
        # self.log += "[*] " + msg + " : " + line + "\n"
        # do the above but with f strings
        self.log += f"[*] {msg} : {line}\n"

    # prints an array with styling
    # the only argument is an array of maps,
    # this is an example:
    #
    # [{'text': 'Hello', 'style': 'bold', 'fore': 'green', 'back': 'blue'},
    # {'text': ' there', 'style': 'italic'}]
    # version : 2.0.386
    def styled_print(self, array):
        global colors
        # set colors if not available for the entire
        # environment
        if not colors:
            # set the colors / styles
            colors = {
                "": "",
                "reset": "\033[0m",
                "black": "\033[30m",
                "red": "\033[31m",
                "green": "\033[32m",
                "yellow": "\033[33m",
                "blue": "\033[34m",
                "magenta": "\033[35m",
                "cyan": "\033[36m",
                "white": "\033[37m",
                "bold": "\033[1m",
                "italic": "\033[3m",
                "underline": "\033[4m",
                "blink": "\033[5m",
            }
        # for each map in the array
        for mp in array:
            # get all the parameters if they exist
            text = mp["text"] if "text" in mp else ""
            # get the style
            style = mp["style"] if "style" in mp else ""
            # get the foreground color
            fore = mp["fore"] if "fore" in mp else ""
            # get the background color
            back = mp["back"] if "back" in mp else ""
            # print the text with the style
            print(
                colors[style]
                + colors[fore]
                + colors[back]
                + str(text)
                + colors["reset"],
                end="",
            )
        # print a newline
        print()

    # checks for and throws a type error
    def type_err(self, values: list[(any, tuple)], line, lines_ran):
        # for each entry in values
        for value, permitted_types in values:
            # if the value is not in the permitted types
            if (current_type := type(value)) not in permitted_types:
                # create string for error
                error_s = ""
                # for each permitted type
                for i, permitted_type in enumerate(permitted_types):
                    # add the type to the error string
                    error_s += str(permitted_type)
                    # if this is not the last type
                    if i != len(permitted_types) - 1:
                        # add a comma
                        error_s += " or "
                # throw error
                self.err(
                    "Incorrect type specified",
                    f"In value: {value}, expected {error_s} got {current_type}",
                    line,
                    lines_ran,
                )

    # general error printing
    def err(self, err, msg, line, lines_ran):
        from core.errors import inter_raise_err
        return inter_raise_err(self, err, msg, inst_tree)

    # throws a keyerror
    def raise_key(self, key, line):
        return self.err(
            "Key not found in dictionary",
            f'Key "{key}" not found in dictionary',
            line,
            lines_ran,
        )

    # throws msn2 error for a work in progress mechanism
    def raise_wip(self, what_is_wip, line, lines_ran):
        # get the version for this interpreter
        return self.err(
            "Work in progress",
            f"{what_is_wip} is a work in progress in MSN2 v{self.version} and not been fully implemented.",
            line,
            lines_ran,
        )

    # verifies a type is iterable
    # iterable types include: list, tuple, dict, set, str

    def check_iterable(self, value, line):
        import collections.abc

        if not isinstance(value, collections.abc.Iterable):
            return self.type_err(
                [(value, (collections.abc.Iterable,))], line, lines_ran
            )
        return True

    # checks for validity of a variable name being set
    # by its string representation
    def check_varname(self, varname, line):
        # varname must be a string
        self.type_err([(varname, (str,))], line, lines_ran)
        # varname must exist
        if not varname:
            self.raise_varname_chars(varname, line, lines_ran)

    # throws an operation error
    def raise_operation_err(self, vname, operator, line):
        # operation error
        return self.err(
            f'Operation error: "{operator}"',
            f'There was an error applying the operator "{operator}" to "{vname}" and its argument(s).\n',
            line,
            lines_ran,
        )

    # throws an error asking for a variable name to at least contain characters

    def raise_varname_chars(self, varname, line, lines_ran):
        return self.err(
            "New variable name must contain characters.",
            f'Variable name "{varname}" is an invalid name.',
            line,
            lines_ran,
        )

    # throws msn2 error for comparison error

    def raise_comp(self, comp_operation, vname, line):
        return self.err(
            "Comparison error",
            f'Could not perform comparison operation "{comp_operation}" on variable "{vname}" and the supplied argument(s)',
            line,
            lines_ran,
        )

    # empty array error

    def raise_empty_array(self, line):
        return self.err("Error computing average", f"Array is empty", line, lines_ran)

    # non_numeric value error

    def raise_avg(self, line):
        return self.err(
            "Error computing average",
            f"Array contains non-numeric values",
            line,
            lines_ran,
        )

    # value is not in the list

    def raise_value(self, value, line):
        return self.err(
            "Value error", f'Value "{value}" is not in the list.', line, lines_ran
        )

    # throws msn2 error for Incorrect number of arguments

    def raise_incorrect_args(self, expected, actual, line, lines_ran, method):
        return self.err(
            f"Incorrect number of function arguments for {method.name}",
            f"Expected {expected}, got {actual}",
            line,
            lines_ran,
        )

    def raise_ArgumentCountError(self, method: str, expected, actual, line, lines_ran):
        return self.err(
            f"Incorrect number of function arguments for {method}",
            f"Expected {expected}, got {actual}",
            line,
            lines_ran,
        )

    # throws msn2 error for Index out of bounds

    def raise_index_out_of_bounds(self, line, lines_ran, method):
        return self.err(
            f"Index out of bounds in body of {method.name if hasattr(method, 'name') else method}",
            f"Index out of bounds",
            line,
            lines_ran,
        )

    def __del__(self):
        None

    def method_args(self, line, j):
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

    def thread_split(self, line):
        self.interpret(line)

    # splits a process
    def process_split(self, line):
        inter = self.new_int()
        return inter.interpret(line)

    # executing Python scripts
    def exec_python(self, python_block, has_outer_function=True, include_temp_vars=True):
        # get the python script with arguments inserted
        py_script = str(self.interpret(
            f"script({python_block})", has_outer_function=has_outer_function, include_temp_vars=include_temp_vars))
        # try to execute the script
        try:
            exec(py_script, self._globals, self._locals)
        except Exception as e:
            # send an error
            self.err("Error running Python script",
                     str(e), py_script, lines_ran)
        return py_script

    def var_exists(self, varname):
        if varname in self.vars:
            return True
        return False

    def var_names(self):
        names = []
        for key in self.vars:
            names.append(key)
        return names

    def is_py_str(self, line):
        try:
            return (line[0] == '"' and line[len(line) - 1] == '"') or (
                line[0] == "'" and line[len(line) - 1] == "'"
            )
        except:
            return False

    def is_str(self, line):
        return line[0] == "<" and line[len(line) - 1] == ">"

    # gets the variable value from the variable name
    def get_var(self, name):
        return self.vars[name].value

    def in_string(self, s, s2):
        return s > 0 or s2 > 0

    # scrapes all html elements from a URL

    def html_all_elements(self, url):
        import requests

        # web scraping
        from bs4 import BeautifulSoup

        # obtains a response from the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html5lib")
        # obtains all html elements
        return soup.find_all()

    def me(self):
        return (
            str(self)
            .replace(" ", "")
            .replace("<", "")
            .replace(">", "")
            .replace("Interpreter", "")
        )

    # prints text with a box around it
    def bordered(text):
        from core.out.utils import bordered
        return bordered(text)
