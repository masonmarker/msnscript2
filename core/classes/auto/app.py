# class for an App

class App:
    # constructor
    def __init__(self, path, application=None, name=None, extension=None):
        # path of application being launched
        self.path = path
        if name:
            self.name = name
            self.extension = extension
        else:
            _spl = path.split("\\")[-1].split(".")
            # extension of the application
            self.extension = _spl[-1]
            self.name = _spl[0]
        # pwinauto application object
        self.application = application