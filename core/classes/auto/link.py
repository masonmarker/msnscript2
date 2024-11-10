# class for a Link

from core.classes.auto.appelement import AppElement


class Link(AppElement):
    # constructor
    def __init__(self, window, name):
        # call super constructor
        super().__init__(window, name)
