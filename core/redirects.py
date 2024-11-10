"""
Redirection functions.
"""

from core.classes.var import Var

# general functions
def f_redirect(inter, line: str, args, **kwargs):
    inter.redirect_inside = []
    # creates redirect for this interpreter
    # check for type errors
    linevar = inter.parse(0, line, args)[2]
    inter.type_err([(linevar, (str,))], line, kwargs["lines_ran"])
    inter.redirect = [linevar, args[1][0]]
    inter.redirecting = True
    return inter.redirect


def f_stopredirect(inter, line: str, args, **kwargs):
    inter.redirecting = False
    return True


def f_startredirect(inter, line: str, args, **kwargs):
    ret = None
    for _ins in inter.redirect_inside:
        inter.vars[inter.redirect[0]] = Var(
            inter.redirect[0], _ins[1])
        ret = inter.interpret(_ins[0])
    return ret

# dispatch
REDIRECTS_DISPATCH = {
    "redirect": f_redirect,
    "stopredirect": f_stopredirect,
    "startredirect": f_startredirect
}
