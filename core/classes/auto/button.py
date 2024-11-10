

# class for a button
from core.classes.auto.appelement import AppElement


class Button(AppElement):
    # constructor
    def __init__(self, window, name):
        # call super constructor
        super().__init__(window, name)

    # clicks the button

    def click(self):
        self.window.click()

    # right clicks the button

    def right_click(self):
        self.window.click_input(button="right")
