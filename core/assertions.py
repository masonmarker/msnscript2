

def assert_err(inter, line, assertion, failed, lines_ran):
    return inter.err(
        f"Assertion error in '{line}'",
        assertion,
        failed,
        lines_ran,
    )


def f_assert(inter, line: str, args, **kwargs):
    for i in range(len(args)):
        assertion = inter.parse(i, line, args)[2]
        if not assertion:
            failed = ""
            for arg in args:
                failed += f"{assertion} "
            assert_err(inter, line, assertion, failed, kwargs["lines_ran"])
    return True


def f_assert_err(inter, line: str, args, **kwargs):
    for i in range(len(args)):
        thrown = True
        try:
            # set inter.trying to True
            inter.trying = True
            # execute the line
            ret = inter.parse(i, line, args)[2]
            thrown = False
            inter.trying = False
        except:
            thrown = True
        if not thrown:
            assert_err(
                inter, line, "No error thrown where one was expected", "", kwargs["lines_ran"])
    return True


ASSERTIONS_DISPATCH = {
    "assert": f_assert,
    "assert:err": f_assert_err,
}
