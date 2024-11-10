
def f_obj_justhtml_gather(inter, line, args, **kwargs):
    # finds elements in the HTML
    if args[0][0] == "":
        return kwargs["object"].find()
    else:
        return kwargs["object"].find(inter.parse(0, line, args)[2])
def f_obj_justhtml_else(inter, line, args, **kwargs):
    return getattr(kwargs["object"], kwargs["objfunc"])


OBJ_GENERAL_CLASS_BASED_REQUESTS_HTML_HTML_DISPATCH = {
    "<class 'requests_html.HTML'>": {
        "gather": f_obj_justhtml_gather,
        "else": f_obj_justhtml_else,
    }
}
