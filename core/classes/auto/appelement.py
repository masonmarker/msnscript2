
# element for an application


class AppElement:
    # constructor
    def __init__(self, window, name):

        # creates a modified window
        self.window = window
        # # set the window
        # self.window = window
        # set the name
        self.name = name

    # gets the text of the window
    def window_text(self):
        return self.name

    # gets all children of the window
    def children(self):
        return self.window.children()

    # sets the focus to the window
    def set_focus(self):
        self.window.set_focus()

    # gets the properties of the window
    def get_properties(self):
        return self.window.get_properties()

    # gets the highest level parent of this element
    def top_level_parent(self):
        return self.window.top_level_parent()

    # computes the height of the window
    def height(self):
        try:
            return (
                self.window.get_properties()["rectangle"].bottom
                - self.window.get_properties()["rectangle"].top
            )
        except:
            return

    # computes the width of the window

    def width(self):
        try:
            return (
                self.window.get_properties()["rectangle"].right
                - self.window.get_properties()["rectangle"].left
            )
        except:
            return

    # string

    def __str__(self):
        from msnint2 import Interpreter
        return Interpreter.bordered(
            f'Text: {self.name if self.name else "[No Text Found]"}\nSize:\
{f"{self.width()}x{self.height()}"}\nObject:\n{self.window}'
        )
