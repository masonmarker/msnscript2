

def f_obj_html_all(inter, line, args, **kwargs):
    # gets information from a website
    return kwargs["object"].get(inter.parse(0, line, args)[2]).html
def f_obj_html_render(inter, line, args, **kwargs):
    # renders the html session
    return kwargs["object"].render(retries=3)
def f_obj_html_else(inter, line, args, **kwargs):
    return kwargs["object"]   


OBJ_GENERAL_CLASS_BASED_REQUESTS_HTML_HTMLSession_DISPATCH = {
    "<class 'requests_html.HTMLSession'>": {
        "all": f_obj_html_all,
        "render": f_obj_html_render,
        "else": f_obj_html_else,
    }
}
