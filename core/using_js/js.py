# Converts MSN2 code to JavaScript.
#
# author : Mason Marker
# date : 12/15/2023
# version : 2.0.400

# html tags and attributes
from core.using_js.js_tools.data.html import html_elements, html_attributes, html_attribute_defaults, css_colors


# returns the representation of parsed input


def parse(inst, i):
    strp = inst.args[i][0].strip()
    if inst.interpreter.is_py_str(strp):
        return f"`{inst.parse(i)}`"
    ret = inst.parse(i)
    if ret is None:
        ret = strp
    return ret


def parse_string(inst, string):
    strp = string.strip()
    if inst.interpreter.is_py_str(strp):
        return f"`{inst.interpreter.interpret(string)}`"
    ret = inst.interpreter.interpret(string)
    if ret is None:
        ret = strp
    return string


def convert_to_js(inst, lock, lines_ran):
    """
    Converts a 'line' of MSN2 code to JavaScript
    """

    # user function execution requested
    if inst.func in inst.interpreter.methods:
        # execute the function
        as_js = f"{inst.func}("
        for i in range(len(inst.args)):
            if i != len(inst.args) - 1:
                as_js += f"{inst.parse(i)}, "
            else:
                as_js += f"{inst.parse(i)}"
        return as_js + ")"
    # if in inst.interpreter.routes
    elif inst.func in inst.interpreter.routes:
        from core.using_js.js_tools.functions import insert_line_at_marker
        # import this route
        raise NotImplementedError
    # if in inst.interpreter.states
    elif inst.obj in inst.interpreter.states:
        state_name = inst.obj
        # get the state value
        state_value = inst.interpreter.states[state_name].value
        if inst.objfunc == 'set':
            from core.using_js.js_tools.functions import generate_safe_set_function
            return generate_safe_set_function(inst, state_name)
        # otherwise, return the state
        return state_name
    elif inst.func == "+":
        return f"({parse(inst, 0)} + {parse(inst, 1)})"
    elif inst.func == "-":
        from core.common import hyphen
        return hyphen(inst)
    # default export code manipulation
    # prettifying code
    elif inst.func == "prettify":
        import jsbeautifier
        # get file path
        file_path = inst.parse(0)
        # get file contents
        with open(file_path, 'r') as f:
            contents = f.read()
        # prettify the contents
        contents = jsbeautifier.beautify(contents, {
            "indent_size": 2,
            "indent_char": " ",
            "indent_with_tabs": False,
            "e4x": True,
            "max_preserve_newlines": 2,
            "preserve_newlines": True,
            "jslint_happy": True
        })
        # write the contents back to the file
        with open(file_path, 'w') as f:
            f.write(contents)
        return ""
    # creates a new css module
    elif inst.func == "css":
        # get root dir
        import os
        from core.using_js.js_tools.functions import get_root_dir, try_add_web_import
        root_dir = get_root_dir(inst)
        # create a styles folder if it doesn't exist
        if not os.path.exists(f"{root_dir}styles"):
            os.mkdir(f"{root_dir}styles")
        # get the name of the css module
        name = inst.parse(0)
        # get the css code
        css_code = parse(inst, 1)
        # get the path to write to
        path = f"{root_dir}styles/{name}.module.css"
        # create the css module
        with open(path, 'w') as f:
            f.write(css_code)
        # add import
        try_add_web_import(
            inst, [(True, name, f"../styles/{name}.module.css")])
        # add the css path to
        return ""
    # uses a UI library
    elif inst.func == "UI":
        # get the _app.js full path from the inst.interpreter vars at react:default:app_path
        app_path = inst.interpreter.vars["react:default:app_path"].value
        # get the UI library name
        ui_name = inst.parse(0)
        # if the name is "chakra"
        if ui_name == "chakra":
            from core.classes.var import Var
            # create a variable saying we're using chakra
            inst.interpreter.vars[_n] = Var(
                (_n := "react:default:_:using_chakra"), True)
            # read from the app path
            initial_app_js = open(app_path, 'r').read()
            # if chakra has not been imported
            if "ChakraProvider" not in initial_app_js:
                from core.using_js.js_tools.functions import insert_line_at_marker
                # im using python to generate a nextjs _app.js, and i need a python function that can append a parent to the returning component, like be able to read from the _app.js file path as an argument, and look at that current javascript and its imports and returning component and stuff, but just rewrite to that file the same code with a new parent element, the HTML tag also being an argument to that function
                # insert the import
                insert_line_at_marker(inst, app_path, "imports",
                                      "import { ChakraProvider } from '@chakra-ui/react';", check_for_dups=True)
                # insert the provider
                insert_line_at_marker(inst, app_path, "return",
                                      "<ChakraProvider>")
                # insert the provider closing tag
                insert_line_at_marker(inst, app_path, "endreturn",
                                      "</ChakraProvider>")
        return ""
    # variables
    # creating a const
    elif inst.func == "const":
        from core.classes.var import Var
        from core.using_js.js_tools.functions import is_react_code
        name = inst.parse(0)
        value = parse(inst, 1)
        # if value is react code
        # create variable in inst.interpreter.vars
        inst.interpreter.vars[name] = Var(
            name, name if not is_react_code else f"{{{name}}}")
        return f"const {name} = {value}\n"
    # let
    elif inst.func == "let":
        from core.classes.var import Var
        from core.using_js.js_tools.functions import is_react_code
        name = inst.parse(0)
        value = parse(inst, 1)
        # if value is react code
        # create variable in inst.interpreter.vars
        inst.interpreter.vars[name] = Var(
            name, name if not is_react_code else f"{{{name}}}")
        return f"let {name} = {value}\n"
    # var
    elif inst.func == "var":
        from core.classes.var import Var
        from core.using_js.js_tools.functions import is_react_code
        name = inst.parse(0)
        value = parse(inst, 1)
        # if value is react code
        # create variable in inst.interpreter.vars
        inst.interpreter.vars[name] = Var(
            name, name if not is_react_code else f"{{{name}}}")
        return f"var {name} = {value}\n"
    # creates a state
    elif inst.func == "state":
        from core.classes.var import Var
        from core.using_js.js_tools.functions import generate_set_function, try_add_web_import, add_state

        # # determine if useState has been imported
        # if (imp := ('useState', 'react')) not in inst.interpreter.web_imports:
        #     from functions import insert_line_at_marker
        #     # insert_line_at_marker()
        #     inst.interpreter.web_imports.add(imp)
        #     # insert the import
        #     insert_line_at_marker(inst, inst.interpreter.next_entry_path, "imports",
        #                           "import { useState } from 'react';", check_for_dups=True)
        #     # insert useEffect
        #     insert_line_at_marker(inst, inst.interpreter.next_entry_path, "imports",
        #                           "import { useEffect } from 'react';", check_for_dups=True)
        try_add_web_import(
            inst, [(False, 'useState', 'react'), (False, 'useEffect', 'react')])
        # get the name of the state
        name = inst.parse(0)
        set_function = generate_set_function(name)
        # default value or new value
        default_value_or_new_value = parse(inst, 1)
        # try to add state
        if (generated := add_state(inst, name, default_value_or_new_value)) != None:
            return generated
        # create new variable
        return f"const [{name}, {set_function}] = useState({default_value_or_new_value})\nuseEffect(() => {{\n// {name} useEffect ::\n}}, [{name}])\n"
    # inserts a useEffect hook
    elif inst.func == "effect":
        from core.using_js.js_tools.functions import use_effect
        return use_effect(inst)
    # states a piece of code as effectful code
    elif inst.func == "effectful":
        # creates a useEffect and a state for this effectful code
        # try to add web import useEffect
        from core.using_js.js_tools.functions import try_add_web_import, generate_serialized_state, generate_set_function, add_state
        try_add_web_import(
            inst, [(False, 'useEffect', 'react'), (False, 'useState', 'react')])
        # get the name of the state
        state_name = inst.parse(0)
        # get the effectful code
        effectful_code = parse(inst, 1)
        # get the default value while this state is not loading
        default_value = parse(inst, 2)
        # create a loading state
        loading_state_script = f"const [{state_name}Loading, {(set_loading := generate_set_function(f'{state_name}Loading'))}] = useState(true)"
        # add state
        add_state(inst, state_name, default_value)
        # get the name of the set function
        set_function = generate_set_function(state_name)
        # create the general state creation script
        state_creation_script = f"const [{state_name}, {set_function}] = useState({default_value})"
        # create the useEffect script to set the serialized state to the effectful code
        use_effect_script = f"useEffect(() => {{(async () => {{\n{set_function}({effectful_code})\n{set_loading}(false);}})();}}, [])"
        # return the loading state, the general state creation script, and the useEffect script
        return f"{loading_state_script};\n{state_creation_script};\n{use_effect_script}"
    # logic
    # if statement returned as && when theres two arguments
    # otherwise returned as ternary operator when theres three arguments
    elif inst.func == "if":
        # get first argument
        first_arg = parse(inst, 0)
        # get second argument
        second_arg = parse(inst, 1)
        # if there is a third argument
        if len(inst.args) == 3:
            # get third argument
            third_arg = parse(inst, 2)
            # return if statement
            return f"({first_arg} ? {second_arg} : {third_arg})"
        # otherwise, return &&
        return f"({first_arg} && {second_arg})"
    # map(iterable, element_varname, (opt) index_varname, js_script) function
    elif inst.func == "map":
        from core.classes.var import Var
        # grab the iterable
        iterable = inst.parse(0)
        # grab the element variable name
        element_varname = inst.parse(1)
        # create element_varname as a variable
        inst.interpreter.vars[element_varname] = Var(
            element_varname, element_varname)
        # if len of args is 4, then there is an index variable name
        if len(inst.args) == 4:
            index_varname = inst.parse(2)
            # create index_varname as a variable
            inst.interpreter.vars[index_varname] = Var(
                index_varname, index_varname)
        else:
            index_varname = None

        return f"{{{iterable}.map(({element_varname}{', ' + index_varname if index_varname else ''}) => \u007breturn {parse(inst, -1)}\u007d)}}"

    # creates a /pages/api/*route*.js file for api interaction
    # also (creates and) appends to /api/functions.js file for api functions
    elif inst.func == "apiroute":
        from core.using_js.js_tools.functions import generate_api_scripts_and_add
        # take input
        route_name = inst.parse(0)
        # route request variable name
        route_req_name = inst.parse(1)
        # route response variable name
        route_res_name = inst.parse(2)
        # generate script from 3rd argument
        script = parse(inst, 3)
        # function fetch body variable name
        fetch_body_name = inst.parse(4)
        # function fetch body script
        fetch_body_script = parse(inst, 5)
        # create the api route function to place at the default export
        # function called when fetched at this route
        # api_route_script = "export default async function " + \
        #     route_name + "(" + route_req_name + ", " + route_res_name + ")  \
        #     {\n" + script + "\n}"
        # # fetches the api route
        # api_func_script = "export async function " + route_name +  \
        #     "(" + fetch_body_name + ") {\nreturn " + fetch_body_script + "\n}"
        generate_api_scripts_and_add(inst, route_name, route_req_name,
                                     route_res_name, script, fetch_body_name, fetch_body_script)
        return ""
    # simpler apiroute
    elif inst.func == "defineapi":
        from core.using_js.js_tools.functions import generate_api_scripts_and_add, generate_fetch
        # take route_name
        route_name = inst.parse(0)
        # take request variable name
        route_req_name = inst.parse(1)
        # take response variable name
        route_res_name = inst.parse(2)
        # take script
        script = parse(inst, 3)
        # create the api route function to place at the default export
        # function called when fetched at this route
        generate_api_scripts_and_add(inst, route_name, route_req_name,
                                     route_res_name, script, 'body', generate_fetch(route_name))
        return ""
    # defines an entire api script at next_project_root/pages/api/*route*.js
    elif inst.func == "defineapiscript":
        from core.using_js.js_tools.functions import generate_api_scripts_and_add, generate_fetch, get_pages_path
        # take route_name
        route_name = inst.parse(0)
        # take initial script
        script = parse(inst, 1)
        # get req name
        req_name = inst.parse(2)
        # get res name
        res_name = inst.parse(3)
        # get function body
        body = parse(inst, 4)
        # create the api route function to place at the default export
        # function called when fetched at this route
        generate_api_scripts_and_add(inst, route_name, req_name,
                                     res_name, body, 'body', generate_fetch(route_name))
        # insert into the new api path
        new_api_path = f"{get_pages_path(inst)}/api/{route_name}.js"
        # get the lines from the api file
        with open(new_api_path, 'r') as f:
            lines = f.readlines()
        # insert script into beginning of file
        lines.insert(0, script)
        # write the lines back to the file
        with open(new_api_path, 'w') as f:
            f.writelines(lines)
        return ""
    # gets from api:route
    elif inst.func == "apiget":
        from core.using_js.js_tools.functions import generate_fetch
        # path to get from
        path = inst.parse(0)
        # request body
        return generate_fetch(inst.parse(0))
    # creates a component route
    elif inst.func == "route":
        from core.using_js.js_tools.functions import add_route
        return add_route(inst, inst.parse(0), inst.parse(1))
    # link to a different page
    elif inst.func == "linkto":
        # import nextlink and useRouter
        from core.using_js.js_tools.functions import try_add_web_import
        # get the page to navigate to
        page = inst.parse(0)
        # remove the first 2 args in inst.args
        # to prepare component
        inst.args = inst.args[1:]
        # add the imports
        try_add_web_import(inst, [(False, 'useRouter', 'next/router'),
                                  (True, 'Link', 'next/link')])
        from core.using_js.js_tools.functions import component
        # return the link
        return component(inst, "Link", {'href': page})
    # grid
    # forces row and columns
    elif inst.func == "grid":
        # get number of rows and columns
        rows = inst.parse(0)
        cols = inst.parse(1)
        # remove the first 2 args in inst.args
        # to prepare component
        inst.args = inst.args[2:]
        # return component
        from core.using_js.js_tools.functions import component
        return component(inst, "div", {'style': {
            'display': 'grid',
            'gridTemplateRows': f"repeat({rows}, 1fr)",
            'gridTemplateColumns': f"repeat({cols}, 1fr)"
        }})
    # creates a page route to a script
    # HTML elements
    elif inst.func in html_elements:
        from core.using_js.js_tools.functions import component
        return component(inst, inst.func)
    # general text
    elif inst.func == "text":
        from core.using_js.js_tools.functions import component
        return component(inst, "span")
    # fits the element to its parent
    elif inst.func == "fitscreen":
        from core.using_js.js_tools.functions import component
        return component(inst, "div", {'style': {
            'height': '100svh',
            'width': '100svw'
        }})
    # vcenter: centers an element vertically
    elif inst.func in ("vcenter", "vcentered"):
        from core.using_js.js_tools.functions import component
        return component(inst, "div", {'style': {
            'display': 'flex',
            'alignItems': 'center',
            'textAlign': 'center',
        }})
    # hcenter: centers an element horizontally
    elif inst.func in ("hcenter", "hcentered"):
        from core.using_js.js_tools.functions import component
        return component(inst, "div", {'style': {
            'display': 'flex',
            'justifyContent': 'center',
            'textAlign': 'center'
        }})
    # centers children both horizontally and vertically
    elif inst.func in ("center", "centered"):
        from core.using_js.js_tools.functions import component
        return component(inst, "div", {'style': {
            'height': 'inherit',
            'width': 'inherit',
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'textAlign': 'center'
        }})
    # vertical stack of components
    elif inst.func == "vstack":
        from core.using_js.js_tools.functions import component
        return component(inst, "div", {'style': {
            'display': 'flex',
            'flexDirection': 'column',
        }})
    # horizontal stack of components
    elif inst.func == "hstack":
        from core.using_js.js_tools.functions import component
        return component(inst, "div", {'style': {
            'display': 'flex',
            'flexDirection': 'row',
        }})
    # REQUIRES REACT 17
    # React.Fragment
    elif inst.func == "fragment":
        from core.using_js.js_tools.functions import component
        return component(inst, "React.Fragment")

    # checking objfunc
    elif inst.obj == "file":
        if inst.objfunc == "write":
            from core.common import file_write
            return file_write(inst, lock, lines_ran)
        elif inst.objfunc == "append":
            from core.common import file_append
            return file_append(inst, lock, lines_ran)
    # imports from an msn2 file
    elif inst.func == "import":
        from core.using_js.js import parse_string
        from core.using_js.js_tools.functions import get_root_dir
        import os
        # get the path of the file
        path = inst.parse(0)
        # get the root dir
        root_dir = get_root_dir(inst)
        # find file
        path = f"{root_dir}msn2/{path}"
        # add .msn2 extension if not already
        if not path.endswith(".msn2"):
            path += ".msn2"
        # get the lines of the file
        with open(path, 'r') as f:
            lines = f.readlines()
        strrep = ""
        for line in lines:
            line = line.strip()
            # if the line is a comment
            if inst.interpreter.is_comment(line):
                continue
            if line:
                strrep += line + "\n"
        # return the string representation of the file
        return inst.interpreter.interpret(strrep)
    # general print, JavaScript equivalent
    # is the notorious 'console.log'
    elif inst.func in ("prnt", "print"):
        from core.using_js.js_tools.functions import stringify
        as_js = "console.log("
        for i in range(len(inst.args)):
            curr = parse(inst, i)
            if not curr:
                curr = inst.args[i][0].strip()
            if i != len(inst.args) - 1:
                as_js += f"{curr},"
            else:
                as_js += curr
        return as_js + ")"
    # queries an html element
    elif inst.func == "query":
        # return "document.querySelector(" + parse(inst, 0) + ")"
        return f"document.querySelector({parse(inst, 0)})"
    # general unnamed function with possible arguments
    elif inst.func == "do":
        # if no arguments
        if inst.args[0][0] == "":
            return "async () => {}"
        # get arguments, aka all arguments except the last
        args = [inst.parse(i) for i in range(len(inst.args) - 1)]
        # get function body, aka the last argument
        body = parse(inst, -1)
        return f"async ({', '.join([str(arg) for arg in args if arg])}) => \u007b{body}\u007d"
    # awaits a function
    elif inst.func == "await":
        return f"await {parse(inst, 0)}"
    # detailed named function with arguments
    elif inst.func == 'def':
        from core.functions import define
        # define the function so it may be recognized as a method
        # in future interpretation
        define(inst, lines_ran)
        as_js = f"function {inst.parse(0)}("
        # last argument is the function body
        for i in range(1, len(inst.args) - 1):
            if i != len(inst.args) - 2:
                as_js += f"{inst.parse(i)}, "
            else:
                as_js += f"{inst.parse(i)}"
        as_js += ") {\n"
        as_js += f"return {inst.parse(-1)}"
        as_js += "}"
        return as_js
    # creates and executes a function in one call
    elif inst.func == "=>" or (inst.func == '' and inst.objfunc == ''):
        from core.using_js.js_tools.functions import callback
        return callback(inst)
    # async function
    elif inst.func == "async":
        from core.using_js.js_tools.functions import callback
        # does the same as the above condition
        # but with async
        return callback(inst, is_async=True)
    # exports a function
    elif inst.func == "export":
        # export the first argument as a string
        return f"export {inst.parse(0)}"
    elif inst.func == "exdefault":
        # export the first argument as a string
        return f"export default {inst.parse(0)}"

    # generates a unique hash based on the current instruction tree
    elif inst.func == "uniquehash":
        from core.using_js.js_tools.functions import unique_hash
        return f"""{unique_hash(inst)}"""

    # REQUIRES REACT 17
    # React.Fragment
    elif inst.func == "unique":
        global inst_tree
        from core.using_js.js_tools.functions import component, unique_hash, try_add_web_import
        # add React import
        try_add_web_import(inst, [(True, 'React', 'react')])
        # return a div with a unique hash
        return component(inst, "React.Fragment", {'key': unique_hash(inst_tree)})
    elif inst.func == "js":
        # just return the first argument
        return f"{{{inst.args[0][0]}}}"
    # renders multiple components in javascript based on an iterable in MSN2.
    #
    # def ('Component', h1('Hello, World!'))
    #
    # render([1, 2, 3], 'x', Component(x))    ->   {[Component(1), Component(2), Component(3)]}
    #
    # # this function does not return a {[0].map()} equivalent, like 'map' does
    # # it returns a "{[Component(0), Component(1), Component(2)]}" equivalent as a PYTHON STRING
    # #
    elif inst.func == "render":
        from core.classes.var import Var
        from core.using_js.js_tools.functions import component, unique_hash_counter
        # get the iterable
        iterable = inst.parse(0)
        # get the variable name
        varname = inst.parse(1)
        # current javascript instruction to return
        js_instruction = ""
        # for each element in the iterable
        for i in range(len(iterable)):
            unique_hash_counter += 1
            # get the element
            element = iterable[i]
            # set the variable to the element
            inst.interpreter.vars[varname] = Var(varname, element)
            # add the instruction to the javascript instruction
            js_instruction += f"{inst.parse(-1)},"
        return f"{{[{js_instruction}]}}"
    # if the function is in the css colors, return a span with the color
    elif inst.func in css_colors:
        from core.using_js.js_tools.functions import component
        return component(inst, "div", {'style': {'color': inst.func}})
    # poppins font
    elif inst.func == "poppins":
        from core.using_js.js_tools.functions import component
        # using chakra icons
        return component(inst, "div", {'style': {'fontFamily': 'Poppins'}})
    elif inst.func.startswith("chakra:icon:"):
        from core.using_js.js_tools.functions import component, try_add_web_import
        # add non default import for @chakra-ui/icons
        name = inst.func.split(":")[2]
        try_add_web_import(inst, [(False, name, '@chakra-ui/icons')])
        return component(inst, name)
    # Chakra elements
    # if the function starts with 'chakra:'
    elif inst.func.startswith("chakra:"):
        from core.using_js.js_tools.functions import component, try_add_web_import
        # get the element name
        element_name = inst.func.split(":")[1]
        try_add_web_import(inst, [(False, element_name, '@chakra-ui/react')])
        # return the component
        return component(inst, element_name)
    # set interpreter using_js to False
    inst.interpreter.using_js = False
    ret = inst.interpret()
    inst.interpreter.using_js = True
    return ret
