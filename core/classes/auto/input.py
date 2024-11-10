# class for Inputs

from core.classes.auto.appelement import AppElement


class Input(AppElement):
    # constructor
    def __init__(self, window, name):
        # call super constructor
        super().__init__(window, name)

    # types text into the input
    def type_keys(self, text):
        self.window.type_keys(text)