def _try_math(inter, func, line, **kwargs):
    try:
        return func()
    except Exception as e:
        return inter.err(
            "Error in math class",
            f"Unable to perform computation\n{e}",
            line,
            kwargs["lines_ran"],
        )

