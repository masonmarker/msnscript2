


def f_auto_largest(inter, line, args, **kwargs):
    elements = inter.parse(0, line, args)[2]
    # elements must be iterable
    inter.check_iterable(elements, line)
    if not elements:
        return elements
    largest = elements[0]
    for element in elements:
        try:
            # element has width and height
            if (
                element.width() > largest.width()
                and element.height() > largest.height()
            ):
                largest = element
        except:
            # element does not have width and height
            return element
    return largest


def f_auto_file(inter, line, args, **kwargs):
    # imports
    import os
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    # you can only run .msn2 scripts
    return askopenfilename(
        initialdir=os.getcwd(),
        filetypes=[("MSN2 Script", "*.msn2")],
    )

OBJ_AUTO_BASIC_DISPATCH = {
    "largest": f_auto_largest,
    "file": f_auto_file,
}