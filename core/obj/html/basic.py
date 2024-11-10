


def f_html_soup(inter, line, args, **kwargs):
    from bs4 import BeautifulSoup
    import requests
    url = inter.parse(0, line, args)[2]
    # url must be str
    inter.type_err([(url, (str,))], line, kwargs["lines_ran"])
    response = requests.get(url)
    return BeautifulSoup(response.content, "html5lib")


def f_html_from(inter, line, args, **kwargs):
    from bs4 import BeautifulSoup
    url = inter.parse(0, line, args)[2]
    # url must be str
    inter.type_err([(url, (str,))], line, kwargs["lines_ran"])
    obj_to_add = []
    all_elem = inter.html_all_elements(url)
    for elem in all_elem:
        obj_to_add.append(
            {
                "tag": elem.name,
                "attrs": elem.attrs,
                "text": elem.text,
            }
        )
    return obj_to_add


def f_html_session(inter, line, args, **kwargs):
    from requests_html import HTMLSession
    return HTMLSession()

OBJ_HTML_BASIC_DISPATCH = {
    "soup": f_html_soup,
    "from": f_html_from,
    "session": f_html_session,
}