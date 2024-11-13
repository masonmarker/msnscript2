"""MSN2 representation of Python's 'NoneType'."""

class Nothing:
    def __eq__(self, other):
        return isinstance(other, Nothing)