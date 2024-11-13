

import os
import subprocess

def retrieve_environment(command, compile_command=None, executable=None):
    if compile_command:
        compiled_code = subprocess.run(
            compile_command,
            capture_output=True,
            text=True
        )
        err = compiled_code.stderr
        if len(err) > 0:
            return {"out": "", "err": err}

    executed_code = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    out = executed_code.stdout
    err = executed_code.stderr
    if len(out) > 0 and out[-1] == "\n":
        out = out[:-1]
    return {"out": out, "err": err}

def f_C(inter, line, args, **kwargs):
    c_code = inter.msn2_replace(args[0][0])
    exec_folder_path = "_exec"
    os.makedirs(exec_folder_path, exist_ok=True)
    file_num = len(os.listdir(exec_folder_path))
    file_name = f"{exec_folder_path}/c{file_num}.c"
    executable = f"{exec_folder_path}/c{file_num}.exe"
    with open(file_name, "w") as f:
        f.write(c_code)
    
    return retrieve_environment(
        command=[executable],
        compile_command=["gcc", file_name, "-o", executable],
        executable=executable
    )

def f_JS(inter, line, args, **kwargs):
    js_code = inter.msn2_replace(args[0][0])
    exec_folder_path = "_exec"
    os.makedirs(exec_folder_path, exist_ok=True)
    file_num = len(os.listdir(exec_folder_path))
    file_name = f"{exec_folder_path}/js{file_num}.js"
    if len(args) == 2:
        file_name = f"{exec_folder_path}/{inter.parse(1, line, args)[2]}.js"
    with open(file_name, "w") as f:
        f.write(js_code)
    
    return retrieve_environment(command=["node", file_name])

def f_JAVA(inter, line, args, **kwargs):
    java_code = inter.msn2_replace(args[0][0])
    exec_folder_path = "_exec"
    os.makedirs(exec_folder_path, exist_ok=True)
    if len(args) == 2:
        java_file_name = inter.parse(1, line, args)[2]
    else:
        file_num = len(os.listdir(exec_folder_path))
        java_file_name = f"java{file_num}"
    file_name = f"{exec_folder_path}/{java_file_name}.java"
    with open(file_name, "w") as f:
        f.write(java_code)
    
    return retrieve_environment(
        command=["java", "-cp", exec_folder_path, java_file_name],
        compile_command=["javac", file_name]
    )



LANG_DISPATCH = {
    "C": f_C,
    "JS": f_JS,
    "JAVA": f_JAVA,
}
