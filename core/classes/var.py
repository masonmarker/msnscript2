
# disallowed variable prefix
RESERVED_VARNAME_PREFIX = "⇰"


class Var:
    # constructs a new Var
    def __init__(self, _msn2_reserved_varname, _msn2_reserved_varvalue, force_allow_name=False):

        # # the variable name cannot start with the msn2 reserved prefix
        # if not force_allow_name and \
        #         hasattr(_msn2_reserved_varname, "startswith") and \
        #         _msn2_reserved_varname.startswith(RESERVED_VARNAME_PREFIX):
        #     raise ValueError(
        #         f"Variable name '{_msn2_reserved_varname}' cannot start with MSN2 reserved special character '{RESERVED_VARNAME_PREFIX}'")

        self.name = _msn2_reserved_varname
        self.value = _msn2_reserved_varvalue

    # determines equality of another Var
    def __eq__(self, other):
        if isinstance(other, Var):
            return other.name == self.name

    # string representation of Var
    def __str__(self):
        return f"(Var {self.name}={self.value})"
