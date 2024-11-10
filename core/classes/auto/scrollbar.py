# class for a scrollbar

from core.classes.auto.appelement import AppElement


class ScrollBar(AppElement):
    # constructor
    def __init__(self, window, name):
        # call super constructor
        super().__init__(window, name)
