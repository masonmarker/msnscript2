


# language functions
def f_C(inter, line, args, **kwargs):
    import os
    # get the C code
    c_code = inter.msn2_replace(args[0][0])
    # create a directory for the C code
    # if it does not exist
    exec_folder_path = "_exec"
    # if the folder does not exist, create it
    if not os.path.exists(exec_folder_path):
        os.mkdir(exec_folder_path)
    # create a file for the C code
    # and write the C code to it
    # get the amount of files in the directory
    # and use that as the file name
    file_num = len(os.listdir(exec_folder_path))
    file_name = f"{exec_folder_path}/c{file_num}.c"
    with open(file_name, "w") as f:
        f.write(c_code)
    # creates a new process
    
    def retrieve_c_environment(c_code):
        import subprocess

        # executable
        executable = f"{exec_folder_path}/c{file_num}.exe"
        # create a new process
        # and execute the C code
        compiled_code = subprocess.run(
            ["gcc", file_name, "-o", executable],
            # capture the output
            capture_output=True,
            text=True,
        )
        # if there's an error, print it
        if len(compiled_code.stderr) > 0:
            return {"out": "", "err": compiled_code.stderr}
        # run the executable
        compiled_code = subprocess.run(
            [executable],
            # capture the output
            capture_output=True,
            text=True,
        )
        # get the output and error
        out = compiled_code.stdout
        err = compiled_code.stderr
        # get the environment
        # env = out.split('\n')[-2]
        # env = env.replace('\'', '"')
        # env = json.loads(env)
        return {"out": out, "err": err}
    
    # execute the C code
    return retrieve_c_environment(c_code)
def f_JS(inter, line, args, **kwargs):
    import os
    # get the JavaScript code
    js_code = inter.msn2_replace(args[0][0])
    # create a directory for the JavaScript code
    # if it does not exist
    exec_folder_path = "_exec"
    # if the folder does not exist, create it
    if not os.path.exists(exec_folder_path):
        os.mkdir(exec_folder_path)
    # create a file for the JavaScript code
    # and write the JavaScript code to it
    # get the amount of files in the directory
    # and use that as the file name
    file_num = len(os.listdir(exec_folder_path))
    file_name = f"{exec_folder_path}/js{file_num}.js"
    # if JS() has two arguments, the second is the name of
    # the file, excluding .js
    if len(args) == 2:
        file_name = (
            f"{exec_folder_path}/{inter.parse(1, line, args)[2]}.js"
        )
    with open(file_name, "w") as f:
        f.write(js_code)
    # creates a new process
    # and executes the JavaScript code
    # returns the environment
    # including the out and variables
    
    def retrieve_js_environment(js_code):
        import subprocess

        # executable
        executable = file_name
        # create a new process
        # and execute the JavaScript code
        compiled_code = subprocess.run(
            ["node", file_name],
            # capture the output
            capture_output=True,
            text=True,
        )
        # get the output and error
        out = compiled_code.stdout
        err = compiled_code.stderr
        # # if there is an error, print it
        # if len(err) > 0:
        #     print(err)
        # remove a succeeding newline
        # if it exists
        if len(out) > 0 and out[-1] == "\n":
            out = out[:-1]
        return {"out": out, "err": err}
    
    # execute the JavaScript code
    return retrieve_js_environment(js_code)
def f_JAVA(inter, line, args, **kwargs):
    import os
    # get the Java code
    java_code = inter.msn2_replace(args[0][0])
    # create a directory for the Java code
    # if it does not exist
    exec_folder_path = "_exec"
    # if the folder does not exist, create it
    if not os.path.exists(exec_folder_path):
        os.mkdir(exec_folder_path)
    # create a file for the Java code
    # and write the Java code to it
    # get the amount of files in the directory
    # and use that as the file name
    file_num = len(os.listdir(exec_folder_path))
    file_name = f"{exec_folder_path}/java{file_num}.java"
    with open(file_name, "w") as f:
        f.write(java_code)
    # creates a new process
    # and executes the Java code
    # returns the environment
    # including the out and variables
    
    def retrieve_java_environment(java_code):
        import subprocess

        # executable
        executable = f"{exec_folder_path}/java{file_num}.class"
        # create a new process
        # and execute the Java code
        compiled_code = subprocess.run(
            ["javac", file_name],
            # capture the output
            capture_output=True,
            text=True,
        )
        # if there's an error, print it
        if len(compiled_code.stderr) > 0:
            return {"out": "", "err": compiled_code.stderr}
        # run the executable
        compiled_code = subprocess.run(
            ["java", executable],
            # capture the output
            capture_output=True,
            text=True,
        )
        # get the output and error
        out = compiled_code.stdout
        err = compiled_code.stderr
        return {"out": out, "err": err}
    
    # execute the Java code
    return retrieve_java_environment(java_code)


LANG_DISPATCH = {
    "C": f_C,
    "JS": f_JS,
    "JAVA": f_JAVA,
}