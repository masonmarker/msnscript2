
def f_next_entry_path(inter, line, args, **kwargs):
    import os
    # if no args
    if args[0][0] == "":
        return inter.next_entry_path
    # otherwise, we're setting it
    inter.next_entry_path = inter.parse(0, line, args)[2]
    # compute and set the next project path, it should be
    # two directories up from the next entry path
    inter.next_project_path = os.path.dirname(
        os.path.dirname(inter.next_entry_path)
    )
    return inter.next_entry_path
def f_next_project_path(inter, line, args, **kwargs):
    return inter.next_project_path




JS_DISPATCH = {
    "next_entry_path": f_next_entry_path,
    "next_project_path": f_next_project_path,    
}