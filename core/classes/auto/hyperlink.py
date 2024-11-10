# class for Hyperlink

from core.classes.auto.appelement import AppElement


class Hyperlink(AppElement):
    # constructor
    def __init__(self, window, name):
        # call super constructor
        super().__init__(window, name)
