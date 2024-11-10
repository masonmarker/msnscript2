"""Windows automation common utilities"""


# basic windows automation elements
from core.classes.auto.appelement import AppElement
from core.classes.auto.hyperlink import Hyperlink
from core.classes.auto.menu import Menu
from core.classes.auto.toolbar import ToolBar
from core.classes.auto.button import Button
from core.classes.auto.link import Link
from core.classes.auto.tabitem import TabItem
from core.classes.auto.table import Table
from core.classes.auto.input import Input


# # GENERAL METHODS
# # gets the immediate children of the parent window

def children(window, parent_window):
    return [
        AppElement(child, child.window_text())
        for child in window.children()
    ]

# gets a child at an index
# prints the children


def child(parent_window, index):
    child = children(parent_window)[index]
    return AppElement(child, child.window_text())

# finds a child with subtext in its name


def find_children(window, parent_window, subtext):
    subtext = subtext.lower()
    return [
        AppElement(child, child.window_text())
        for child in window.children()
        if subtext in child.window_text().lower()
    ]

# recursively searches the child tree for a certain object type
# dont allow ElementAmbiguousError


def recursive_search(
    parent_window, type, as_type, object_string_endswith=None
):
    found = []
    # get the children
    # use kwargs to avoid ElementAmbiguousError
    # kwargs is a criteria to reduce a list by process, class_name, control_type, content_only and/or title.
    kwargs = {"process": parent_window.process_id()}
    c = parent_window.children(**kwargs)
    for child in c:
        if isinstance(child, type) or (
            object_string_endswith
            and str(child).endswith(object_string_endswith)
        ):
            found += [as_type(child, child.window_text())]
        found += recursive_search(
            child, type, as_type, object_string_endswith
        )
    return found

# prints all elements


def print_elements(parent_window, retrieve_elements):
    for i, element in enumerate(retrieve_elements(parent_window)):
        print(i, ":")
        print(element)
    return None

# finds an element containing the substring specified


def find_elements(parent_window, subtext, retrieve_elements):
    elements = []
    subtext = subtext.lower()
    for element in retrieve_elements(parent_window):
        if subtext in element.name.lower():
            elements.append(
                AppElement(element, element.window_text())
            )
    return elements

# finds the exact elements specified


def find_elements_exact(parent_window, text, retrieve_elements):
    elements = []
    for element in retrieve_elements(parent_window):
        if text == element.name:
            elements.append(
                AppElement(element, element.window_text())
            )
    return elements

# waits for the first element to appear containing the substring specified
# is not case sensitive


def wait_for_element_subtext(
    parent_window, retrieve_elements, subtext, timeout=None
):
    subtext = subtext.lower()
    # subfunction for locating the element

    def find_element_():
        try:
            for element in retrieve_elements(parent_window):
                if subtext in element.name.lower():
                    return AppElement(
                        element, element.window_text()
                    )
        except:
            pass

    if not timeout:
        while True:
            if (_ret := find_element_()) is not None:
                return _ret
    else:
        import time

        # get the current time
        start_time = time.time()
        # while the time elapsed is less than the timeout
        while time.time() - start_time < timeout:
            if (_ret := find_element_()) is not None:
                return _ret

# waits for the first element to appear with the exact text specified


def wait_for_element_exact(
    parent_window, retrieve_elements, text, timeout=None
):
    # subfunction for locating the element
    def find_element_():
        try:
            for element in retrieve_elements(parent_window):
                if text == element.name:
                    return AppElement(
                        element, element.window_text()
                    )
        except:
            pass

    if not timeout:
        while True:
            if (_ret := find_element_()) is not None:
                return _ret
    else:
        import time

        # get the current time
        start_time = time.time()
        # while the time elapsed is less than the timeout
        while time.time() - start_time < timeout:
            if (_ret := find_element_()) is not None:
                return _ret

# waits for the first element to appear in all children containing the substring specified with the type specified


def wait_for_type_subtext_all(
    parent_window, type, as_type, subtext, timeout=None
):
    return wait_for_element_subtext(
        parent_window,
        lambda parent_window: recursive_search(
            parent_window, type, as_type
        ),
        subtext,
        timeout=timeout,
    )

# wait for the first element to appear in all children with the exact text specified with the type specified


def wait_for_type_exact_all(
    parent_window, type, as_type, text, timeout=None
):
    return wait_for_element_exact(
        parent_window,
        lambda parent_window: recursive_search(
            parent_window, type, as_type
        ),
        text,
        timeout=timeout,
    )

# waits for a child to exist with text containing subtext


def wait_for_text(parent_window, subtext, timeout=None):
    return wait_for_element_subtext(
        parent_window, children, subtext, timeout=timeout
    )

# waits for a child to exist in the entire child tree containing subtext


def wait_for_text_all(parent_window, subtext, timeout=None):
    return wait_for_element_subtext(
        parent_window, all_children, subtext, timeout=timeout
    )

# waits for a child to exist with text exactly equal to text


def wait_for_text_exact(parent_window, text, timeout=None):
    return wait_for_element_exact(
        parent_window, children, text, timeout=timeout
    )

# waits for a child to exist in the entire child tree with text exactly equal to text


def wait_for_text_exact_all(parent_window, text, timeout=None):
    return wait_for_element_exact(
        parent_window, all_children, text, timeout=timeout
    )

# prints all children of a parent window


def print_children(parent_window):
    return print_elements(parent_window, children)

# gets all children in the child tree


def all_children(parent_window):
    found = []
    for child in parent_window.children():
        found.append(AppElement(child, child.window_text()))
        found += all_children(child)
    return found

# prints the child tree of a parent window


def print_all_children(parent_window):
    return print_elements(parent_window, all_children)

# gets from all children at an index


def all_child(parent_window, index):
    return all_children(parent_window)[index]

# finds all children with subtext in their name


def find_all_children(parent_window, subtext):
    return find_elements(parent_window, subtext, all_children)

# finds all children from an exact text


def find_all_children_exact(parent_window, text):
    return find_elements_exact(parent_window, text, all_children)

# ---------------------------

# NARROWING GENERAL METHODS
# recursively gets all menus existing in the parent_window tree
# accumulates all instances of pywinauto.controls.uia_controls.MenuWrapper


def menus(parent_window):
    import pywinauto
    return recursive_search(
        parent_window,
        pywinauto.controls.uia_controls.MenuWrapper,
        Menu,
    )

# gets a single menu


def menu(parent_window, index):
    return menus(parent_window)[index]

# prints all the menus


def print_menus(parent_window):
    return print_elements(parent_window, menus)

# finds a menu with subtext in its name


def find_menus(parent_window, subtext):
    return find_elements(parent_window, subtext, menus)

# gets all toolbars


def toolbars(parent_window):
    import pywinauto
    return recursive_search(
        parent_window,
        pywinauto.controls.uia_controls.ToolbarWrapper,
        ToolBar,
    )


def print_toolbars(parent_window):
    return print_elements(parent_window, toolbars)


def toolbar(parent_window, index):
    return toolbars(parent_window)[index]


def find_toolbars(parent_window, subtext):
    return find_elements(parent_window, subtext, toolbars)

# recursively gets all instances of pywinauto.controls.uia_controls.ButtonWrapper


def buttons(parent_window):
    import pywinauto
    return recursive_search(
        parent_window,
        pywinauto.controls.uia_controls.ButtonWrapper,
        Button,
    )


def button(parent_window, index):
    return buttons(parent_window)[index]


def print_buttons(parent_window):
    return print_elements(parent_window, buttons)


def find_buttons(parent_window, subtext):
    return find_elements(parent_window, subtext, buttons)

# for hyperlinks


def links(parent_window):
    return recursive_search(
        parent_window,
        int,
        Link,
        object_string_endswith="Hyperlink",
    )


def link(parent_window, index):
    return links(parent_window)[index]


def print_links(parent_window):
    return print_elements(parent_window, links)


def find_links(parent_window, subtext):
    return find_elements(parent_window, subtext, links)


def find_links_exact(parent_window, text):
    return find_elements_exact(parent_window, text, links)

# for tabitems


def tabitems(parent_window):
    return recursive_search(
        parent_window,
        int,
        TabItem,
        object_string_endswith="TabItem",
    )


def tabitem(parent_window, index):
    return tabitems(parent_window)[index]


def print_tabitems(parent_window):
    return print_elements(parent_window, tabitems)


def find_tabitems(parent_window, subtext):
    return find_elements(parent_window, subtext, tabitems)


def find_tabitems_exact(parent_window, text):
    return find_elements_exact(parent_window, text, tabitems)

# for tabcontrols


def tabcontrols(parent_window):
    return recursive_search(
        parent_window,
        int,
        AppElement,
        object_string_endswith="TabControl",
    )


def tabcontrol(parent_window, index):
    return tabcontrols(parent_window)[index]


def print_tabcontrols(parent_window):
    return print_elements(parent_window, tabcontrols)


def find_tabcontrols(parent_window, subtext):
    return find_elements(parent_window, subtext, tabcontrols)


def find_tabcontrols_exact(parent_window, text):
    return find_elements_exact(parent_window, text, tabcontrols)

# for EditWrapper


def inputs(parent_window):
    import pywinauto
    return recursive_search(
        parent_window,
        pywinauto.controls.uia_controls.EditWrapper,
        Input,
    )


def input(parent_window, index):
    return inputs(parent_window)[index]


def print_inputs(parent_window):
    return print_elements(parent_window, inputs)


def find_inputs(parent_window, subtext):
    return find_elements(parent_window, subtext, inputs)


def find_inputs_exact(parent_window, text):
    return find_elements_exact(parent_window, text, inputs)

# for ButtonWrapper but endswith CheckBox


def checkboxes(parent_window):
    return recursive_search(
        parent_window,
        int,
        Button,
        object_string_endswith="CheckBox",
    )


def checkbox(parent_window, index):
    return checkboxes(parent_window)[index]


def print_checkboxes(parent_window):
    return print_elements(parent_window, checkboxes)


def find_checkboxes(parent_window, subtext):
    return find_elements(parent_window, subtext, checkboxes)


def find_checkboxes_exact(parent_window, text):
    return find_elements_exact(parent_window, text, checkboxes)

# for Image


def images(parent_window):
    return recursive_search(
        parent_window,
        int,
        AppElement,
        object_string_endswith="Image",
    )


def image(parent_window, index):
    return images(parent_window)[index]


def print_images(parent_window):
    return print_elements(parent_window, images)


def find_images(parent_window, subtext):
    return find_elements(parent_window, subtext, images)


def find_images_exact(parent_window, text):
    return find_elements_exact(parent_window, text, images)

# for Tables


def tables(parent_window):
    return recursive_search(
        parent_window,
        int,
        Table,
        object_string_endswith="Table",
    )


def table(parent_window, index):
    return tables(parent_window)[index]


def print_tables(parent_window):
    return print_elements(parent_window, tables)


def find_tables(parent_window, subtext):
    return find_elements(parent_window, subtext, tables)


def find_tables_exact(parent_window, text):
    return find_elements_exact(parent_window, text, tables)

# for GroupBoxes


def groupboxes(parent_window):
    return recursive_search(
        parent_window,
        int,
        AppElement,
        object_string_endswith="GroupBox",
    )


def groupbox(parent_window, index):
    return groupboxes(parent_window)[index]


def print_groupboxes(parent_window):
    return print_elements(parent_window, groupboxes)


def find_groupboxes(parent_window, subtext):
    return find_elements(parent_window, subtext, groupboxes)


def find_groupboxes_exact(parent_window, text):
    return find_elements_exact(parent_window, text, groupboxes)

# for Panes


def panes(parent_window):
    return recursive_search(
        parent_window,
        int,
        AppElement,
        object_string_endswith="Pane",
    )


def pane(parent_window, index):
    return panes(parent_window)[index]


def print_panes(parent_window):
    return print_elements(parent_window, panes)


def find_panes(parent_window, subtext):
    return find_elements(parent_window, subtext, panes)


def find_panes_exact(parent_window, text):
    return find_elements_exact(parent_window, text, panes)

# for ListItems


def listitems(parent_window):
    import pywinauto
    return recursive_search(
        parent_window,
        pywinauto.controls.uia_controls.ListItemWrapper,
        AppElement,
        object_string_endswith="ListItem",
    )


def listitem(parent_window, index):
    return listitems(parent_window)[index]


def print_listitems(parent_window):
    return print_elements(parent_window, listitems)


def find_listitems(parent_window, subtext):
    return find_elements(parent_window, subtext, listitems)


def find_listitems_exact(parent_window, text):
    return find_elements_exact(parent_window, text, listitems)

# for documents


def documents(parent_window):
    return recursive_search(
        parent_window,
        int,
        AppElement,
        object_string_endswith="Document",
    )


def document(parent_window, index):
    return documents(parent_window)[index]


def print_documents(parent_window):
    return print_elements(parent_window, documents)


def find_documents(parent_window, subtext):
    return find_elements(parent_window, subtext, documents)


def find_documents_exact(parent_window, text):
    return find_elements_exact(parent_window, text, documents)

# for decendants


def descendants(parent_window):
    return recursive_search(parent_window, int, AppElement)

# # ---------------------------
# # GENERALIZING METHOD CALLS FOR ELEMENT DISCOVERY


def callables(
    window,
    # array elements
    objfunc1,
    objfunc1_method,
    # print the elements
    objfunc2,
    objfunc2_method,
    # get a certain element
    objfunc3,
    objfunc3_method,
    # find elements with subtext in their names
    objfunc4,
    objfunc4_method,
    # find elements with exact text in their names
    objfunc5=None,
    objfunc5_method=None,
    # waits for the first element of a certain type with subtext in name
    objfunc6=None,
    objfunc6_method=None,
    type1=None,
    as_type1=None,
    # waits for the first element of a certain type with exact text in name
    objfunc7=None,
    objfunc7_method=None,
    type2=None,
    as_type2=None,
    **kwargs
):

    # RETRIEVING CHILDREN
    # gets the available child reference keywords
    if kwargs["objfunc"] == objfunc1:
        return objfunc1_method(window)
    # prints the children
    if kwargs["objfunc"] == objfunc2:
        return objfunc2_method(window)
    # gets a certain child
    # first argument is the index of the child
    if kwargs["objfunc"] == objfunc3:
        return objfunc3_method(window, kwargs["inter"].parse(0, kwargs["line"], kwargs["args"])[2])
    # finds children with subtext in their names
    if kwargs["objfunc"] == objfunc4:
        return objfunc4_method(window, kwargs["inter"].parse(0, kwargs["line"], kwargs["args"])[2])
    if kwargs["objfunc"] == objfunc5:
        return objfunc5_method(window, kwargs["inter"].parse(0, kwargs["line"], kwargs["args"])[2])

    # waits for the first child of a certain type with exact text in its name
    if kwargs["objfunc"] == objfunc6:
        # if 1 argument, there is no timeout
        if len(kwargs["args"]) == 1:
            return wait_for_type_exact_all(
                window,
                type1,
                as_type1,
                kwargs["inter"].parse(0, kwargs["line"], kwargs["args"])[2],
            )
        elif len(kwargs["args"]) == 2:
            return wait_for_type_exact_all(
                window,
                type1,
                as_type1,
                kwargs["inter"].parse(0, kwargs["line"], kwargs["args"])[2],
                kwargs["inter"].parse(1, kwargs["line"], kwargs["args"])[2],
            )
    # waits for the first child of a certain type with subtext in its name
    if kwargs["objfunc"] == objfunc7:
        # if 1 argument, there is no timeout
        if len(kwargs["args"]) == 1:
            return wait_for_type_subtext_all(
                window,
                type2,
                as_type2,
                kwargs["inter"].parse(0, kwargs["line"], kwargs["args"])[2],
            )
        elif len(kwargs["args"]) == 2:
            return wait_for_type_subtext_all(
                window,
                type2,
                as_type2,
                kwargs["inter"].parse(0, kwargs["line"], kwargs["args"])[2],
                kwargs["inter"].parse(1, kwargs["line"], kwargs["args"])[2],
            )

    return "<msnint2 no callable>"

# ---------------------------

# moves the mouse to the center of an element, and clicks it


def clk(window, button="left", waittime=0):
    import time
    from pywinauto import mouse

    # set the focus to this element
    window.set_focus()
    # wait for the element to be ready
    time.sleep(waittime)
    # get the new coordinates of this element after the focus
    coords = window.get_properties()["rectangle"].mid_point()
    # click the mouse
    mouse.click(button=button, coords=coords)
    # return the object
    return object

# determines if a point is visible within a rectangle


def has_point(object, x, y):
    try:
        rect = object.get_properties()["rectangle"]
        # if implemented
        return (
            rect.top <= y <= rect.bottom
            and rect.left <= x <= rect.right
        )
    except:
        print(str(object))
        return True

# recursively get the first object that has the point
# the first object that has the point and no children


def rec(root, x, y):
    # if the root has children
    if root.children():
        # for each child
        for child in root.children():
            # if the child has the point
            if has_point(child, x, y):
                # return the child
                return rec(child, x, y)
    # if the root has no children
    else:
        # return the root
        return AppElement(root, root.window_text())

# get all objects that have the point


def get_all(root, x, y):
    all = []
    # if the root has children
    if root.children():
        # for each child
        for child in root.children():
            # if the child has the point
            if has_point(child, x, y):
                # add the child to the list
                all.append(
                    AppElement(child, child.window_text())
                )
                # get all of the child's children
                all += get_all(child, x, y)
    # return the list
    return all

# presses multiple keys at the same time


def press_simul(kys):
    sending = ""
    # keys down
    for key in kys:
        sending += "{" + key + " down}"
    # keys up
    for key in kys:
        sending += "{" + key + " up}"
    return sending

# function for converting keys requiring a shift press
#   example: a '3' should be converted to {VK_SHIFT down}3{VK_SHIFT up}
#   example: a '"' should be converted to {VK_SHIFT down}'{VK_SHIFT up}
#   example: a 'E' should be converted to {VK_SHIFT down}e{VK_SHIFT up}
# this function is mainly for converting an exerpt of code to a typable
# string for pywinauto to type


def convert_keys(keystrokes):
    new = ""
    special = {
        "!": "1",
        "@": "2",
        "#": "3",
        "$": "4",
        "%": "5",
        "^": "6",
        "&": "7",
        "*": "8",
        "(": "9",
        ")": "0",
        "_": "-",
        "+": "=",
        "{": "[",
        "}": "]",
        "|": "\\",
        ":": ";",
        '"': "'",
        "<": ",",
        ">": ".",
        "?": "/",
        "~": "`",
        " ": " ",
    }
    # for each keystroke
    for key in keystrokes:
        if key == " ":
            # if the key is a space
            new += " "
        elif key in special:
            # if the key is a special character
            new += (
                "{VK_SHIFT down}" + special[key] + "{VK_SHIFT up}"
            )
        elif key.isupper():
            # if the key is uppercase
            new += "{VK_SHIFT down}" + key.lower() + "{VK_SHIFT up}"
        else:
            # if the key is not a special character
            new += key
    return new

# types keys with a delay between each key


def type_keys_with_delay(window, text, delay):
    e = False
    import time
    import pywinauto

    for char in text:
        try:
            window.type_keys(char, with_spaces=True)
        except:
            if not e:
                window.set_focus()
                e = True
            pywinauto.keyboard.send_keys(char)
        time.sleep(delay)

# parses object functions for discovering types
# of elements


def search(window, **kwargs):
    import pywinauto

    ret = "<msnint2 no callable>"
    # RETRIEVING CHILDREN
    # gets the available child reference keywords
    if (
        chldrn := callables(
            window,
            "children",
            children,
            "print_children",
            print_children,
            "child",
            child,
            "find_children",
            find_children,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = chldrn
    # working with the entire child tree
    elif (
        all_chldrn := callables(
            window,
            "all_children",
            all_children,
            "print_all_children",
            print_all_children,
            "all_child",
            all_child,
            "find_all_children",
            find_all_children,
            "find_all_children_exact",
            find_all_children_exact,
            objfunc6="wait_for_child",
            objfunc6_method=wait_for_type_exact_all,
            type1=pywinauto.controls.uiawrapper.UIAWrapper,
            as_type1=AppElement,
            objfunc7="wait_for_child_exact",
            objfunc7_method=wait_for_type_subtext_all,
            type2=pywinauto.controls.uiawrapper.UIAWrapper,
            as_type2=AppElement,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = all_chldrn
    # getting all menus
    elif (
        mns := callables(
            window,
            "menus",
            menus,
            "print_menus",
            print_menus,
            "menu",
            menu,
            "find_menus",
            find_menus,
            objfunc5=None,
            objfunc5_method=None,
            objfunc6="wait_for_menu_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=pywinauto.controls.uia_controls.MenuWrapper,
            as_type1=Menu,
            objfunc7="wait_for_menu",
            objfunc7_method=wait_for_type_subtext_all,
            type2=pywinauto.controls.uia_controls.MenuWrapper,
            as_type2=Menu,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = mns
    # gets all toolbars
    elif (
        tbrs := callables(
            window,
            "toolbars",
            toolbars,
            "print_toolbars",
            print_toolbars,
            "toolbar",
            toolbar,
            "find_toolbars",
            find_toolbars,
            objfunc5=None,
            objfunc5_method=None,
            objfunc6="wait_for_toolbar_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=pywinauto.controls.uia_controls.ToolbarWrapper,
            as_type1=ToolBar,
            objfunc7="wait_for_toolbar",
            objfunc7_method=wait_for_type_subtext_all,
            type2=pywinauto.controls.uia_controls.ToolbarWrapper,
            as_type2=ToolBar,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = tbrs
    # gets all buttons
    elif (
        btns := callables(
            window,
            "buttons",
            buttons,
            "print_buttons",
            print_buttons,
            "button",
            button,
            "find_buttons",
            find_buttons,
            objfunc5=None,
            objfunc5_method=None,
            objfunc6="wait_for_button_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=pywinauto.controls.uia_controls.ButtonWrapper,
            as_type1=Button,
            objfunc7="wait_for_button",
            objfunc7_method=wait_for_type_subtext_all,
            type2=pywinauto.controls.uia_controls.ButtonWrapper,
            as_type2=Button,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = btns
    # gets all tabitems
    elif (
        tbs := callables(
            window,
            "tabitems",
            tabitems,
            "print_tabitems",
            print_tabitems,
            "tabitem",
            tabitem,
            "find_tabitems",
            find_tabitems,
            objfunc5=None,
            objfunc5_method=None,
            objfunc6="wait_for_tabitem_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=int,
            as_type1=TabItem,
            objfunc7="wait_for_tabitem",
            objfunc7_method=wait_for_type_subtext_all,
            type2=int,
            as_type2=TabItem,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = tbs
    # gets all links
    elif (
        lnks := callables(
            window,
            "links",
            links,
            "print_links",
            print_links,
            "link",
            link,
            "find_links",
            find_links,
            objfunc5=None,
            objfunc5_method=None,
            objfunc6="wait_for_link_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=int,
            as_type1=Hyperlink,
            objfunc7="wait_for_link",
            objfunc7_method=wait_for_type_subtext_all,
            type2=int,
            as_type2=Hyperlink,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = lnks
    # gets all Inputs
    elif (
        inpts := callables(
            window,
            "inputs",
            inputs,
            "print_inputs",
            print_inputs,
            "input",
            input,
            "find_inputs",
            find_inputs,
            objfunc6="wait_for_input_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=pywinauto.controls.uia_controls.EditWrapper,
            as_type1=Input,
            objfunc7="wait_for_input",
            objfunc7_method=wait_for_type_subtext_all,
            type2=pywinauto.controls.uia_controls.EditWrapper,
            as_type2=Input,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = inpts
    # gets all checkboxes
    elif (
        chks := callables(
            window,
            "checkboxes",
            checkboxes,
            "print_checkboxes",
            print_checkboxes,
            "checkbox",
            checkbox,
            "find_checkboxes",
            find_checkboxes,
            objfunc6="wait_for_checkbox_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=pywinauto.controls.uia_controls.ButtonWrapper,
            as_type1=Button,
            objfunc7="wait_for_checkbox",
            objfunc7_method=wait_for_type_subtext_all,
            type2=pywinauto.controls.uia_controls.ButtonWrapper,
            as_type2=Button,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = chks
    # gets all images
    elif (
        imgs := callables(
            window,
            "images",
            images,
            "print_images",
            print_images,
            "image",
            image,
            "find_images",
            find_images,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = imgs
    # gets all tables
    elif (
        tbls := callables(
            window,
            "tables",
            tables,
            "print_tables",
            print_tables,
            "table",
            table,
            "find_tables",
            find_tables,
            objfunc6="wait_for_table_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=pywinauto.controls.uia_controls.ListViewWrapper,
            as_type1=Table,
            objfunc7="wait_for_table",
            objfunc7_method=wait_for_type_subtext_all,
            type2=pywinauto.controls.uia_controls.ListViewWrapper,
            as_type2=Table,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = tbls
    # get all GroupBoxes
    elif (
        grps := callables(
            window,
            "groupboxes",
            groupboxes,
            "print_groupboxes",
            print_groupboxes,
            "groupbox",
            groupbox,
            "find_groupboxes",
            find_groupboxes,
            objfunc6="wait_for_groupbox_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=int,
            as_type1=AppElement,
            objfunc7="wait_for_groupbox",
            objfunc7_method=wait_for_type_subtext_all,
            type2=int,
            as_type2=AppElement,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = grps
    # for Panes
    elif (
        pns := callables(
            window,
            "panes",
            panes,
            "print_panes",
            print_panes,
            "pane",
            pane,
            "find_panes",
            find_panes,
            objfunc6="wait_for_pane_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=int,
            as_type1=AppElement,
            objfunc7="wait_for_pane",
            objfunc7_method=wait_for_type_subtext_all,
            type2=int,
            as_type2=AppElement,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = pns
    # for ListItems
    elif (
        lsts := callables(
            window,
            "listitems",
            listitems,
            "print_listitems",
            print_listitems,
            "listitem",
            listitem,
            "find_listitems",
            find_listitems,
            objfunc6="wait_for_listitem_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=pywinauto.controls.uia_controls.ListItemWrapper,
            as_type1=AppElement,
            objfunc7="wait_for_listitem",
            objfunc7_method=wait_for_type_subtext_all,
            type2=pywinauto.controls.uia_controls.ListItemWrapper,
            as_type2=AppElement,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = lsts
    # for TabControls
    elif (
        tabs := callables(
            window,
            "tabcontrols",
            tabcontrols,
            "print_tabcontrols",
            print_tabcontrols,
            "tabcontrol",
            tabcontrol,
            "find_tabcontrols",
            find_tabcontrols,
            objfunc6="wait_for_tabcontrol_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=int,
            as_type1=AppElement,
            objfunc7="wait_for_tabcontrol",
            objfunc7_method=wait_for_type_subtext_all,
            type2=int,
            as_type2=AppElement,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = tabs
    # for Documents
    elif (
        docs := callables(
            window,
            "documents",
            documents,
            "print_documents",
            print_documents,
            "document",
            document,
            "find_documents",
            find_documents,
            objfunc6="wait_for_document_exact",
            objfunc6_method=wait_for_type_exact_all,
            type1=int,
            as_type1=AppElement,
            objfunc7="wait_for_document",
            objfunc7_method=wait_for_type_subtext_all,
            type2=int,
            as_type2=AppElement,
            **kwargs
        )
    ) != "<msnint2 no callable>":
        ret = docs
    return ret


def movemouse(start, end, speed):
    import time
    from pywinauto import mouse

    # reverse the speed, so a speed of 50 gives
    # end_range of 50, and a speed of 75 gives
    # end_range of 25
    # dragging the mouse
    # presses the mouse down at the coordinates
    mouse.press(coords=start)
    end_range = 100 - speed
    for i in range(0, end_range):
        mouse.move(
            coords=(
                int(start[0] + (end[0] - start[0]) / 100 * i),
                int(start[1] + (end[1] - start[1]) / 100 * i),
            )
        )
        time.sleep(0.001)

    # releases the mouse at the end coordinates
    mouse.release(coords=end)


def _prepare_app(inter, line, args, **kwargs):
    ret = kwargs["object"]
    objfunc = kwargs["objfunc"]
    path = kwargs["object"].path
    app = kwargs["object"].application
    window = app.window() if app else None

    # thread based operation
    p_thread = False
    if objfunc.endswith(":lock"):
        p_thread = True
        objfunc = objfunc[:-5]
        kwargs["auto_lock"].acquire()
    search_queried = False
    if (srch := search(window, **{**kwargs, "inter": inter, "line": line, "args": args})) != "<msnint2 no callable>":
        ret = srch
        search_queried = True
    return ret, objfunc, path, app, window, search_queried, p_thread


def _prepare_appelement(inter, line, args, **kwargs):
    ret = kwargs["object"]
    window = kwargs["object"].element
    objfunc = kwargs["objfunc"]
    name = kwargs["object"].name

    p_thread = False
    if objfunc.endswith(":lock"):
        p_thread = True
        objfunc = objfunc[:-5]
        kwargs["auto_lock"].acquire()
    search_queried = False
    if (srch := search(window, **{**kwargs, "inter": inter, "line": line, "args": args})) != "<msnint2 no callable>":
        ret = srch
        search_queried = True
    return ret, objfunc, name, window, p_thread, search_queried


def _prepare_button(inter, line, args, **kwargs):
    window = kwargs["object"]
    p_thread = False
    if kwargs["objfunc"].endswith(":lock"):
        p_thread = True
        kwargs["objfunc"] = kwargs["objfunc"][:-5]
        kwargs["auto_lock"].acquire()
    return window, p_thread


def _prepare_link(inter, line, args, **kwargs):
    window, p_thread = _prepare_button(inter, line, args, **kwargs)
    waittime = (
        inter.parse(0, line, args)[2] if args[0][0] != "" else 1
    )
    # waittime should be float or int or complex
    inter.type_err(
        [(waittime, (float, int, complex))], line, kwargs["lines_ran"]
    )
    return window, waittime, p_thread


def _prepare_table(inter, line, args, **kwargs):
    window, p_thread = _prepare_button(inter, line, args, **kwargs)
    table = kwargs["object"].window
    return window, table, p_thread


def _prepare_toolbars(inter, line, args, **kwargs):
    window, p_thread = _prepare_button(inter, line, args, **kwargs)
    return window, p_thread


def _prepare_scrollbars(inter, line, args, **kwargs):
    window, p_thread = _prepare_button(inter, line, args, **kwargs)
    return window, p_thread
