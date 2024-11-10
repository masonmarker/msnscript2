# class for TabItems

from core.classes.auto.appelement import AppElement


class TabItem(AppElement):
    # constructor
    def __init__(self, window, name):
        # call super constructor
        super().__init__(window, name)