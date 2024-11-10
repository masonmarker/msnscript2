"""In-lang functions for the container object."""




def f_obj_general_container_run(inter, line, args, **kwargs):
    # get the container, which should be the first argument
    kwargs["object"].run()



OBJ_GENERAL_CONTAINER_DISPATCH = {
    'run': f_obj_general_container_run,
}