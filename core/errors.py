from core.out.utils import bordered


def inter_raise_err(inter, err, msg, inst_tree):
    from core.classes.exceptions.msn2exception import MSN2Exception
    # if we're not trying something, and there's an error,
    # print the error
    if not inter.trying:
        # the total words printed for this error
        words_printed = ""
        # max subinstructions to show
        MAX_SUBINSTRUCTIONS = 14

        # prints the error

        def print_err(array):
            # print the error
            inter.styled_print(array)
            # add to words printed
            nonlocal words_printed
            words_printed += str(array)

        # printing the traceback
        print_err(
            [
                {"text": "MSN2 Traceback:\n", "style": "bold", "fore": "green"},
                {"text": (divider := "-" * 15),
                 "style": "bold", "fore": "green"},
            ]
        )
        _branches = []
        root_nums = {root_num for _, (root_num, _) in inst_tree.items()}
        # for k, (root_num, code_line) in inst_tree.items():
        #     root_nums.add(root_num)
        # #root_nums = list(set(root_nums))
        # #root_nums.sort()
        for root_num in sorted(root_nums):
            branches = []
            for k, (root_num2, code_line2) in inst_tree.items():
                if root_num2 == root_num:
                    branches.append(code_line2)
            _branches.append(branches)
        # print the traceback
        # only the last 7 branches
        for i, _branch in enumerate((new_branches := _branches[-7:])):
            # color of the text
            _branch_color = "black"
            # if this is the last branch
            if is_caller := i == len(new_branches) - 1:
                _branch_color = "red"
            else:
                _branch_color = "white"
            # print the caller
            if (_b := _branch[0].strip()) != "":
                print_err(
                    [
                        {"text": ">> ", "style": "bold", "fore": "black"},
                        {
                            "text": inter.shortened(_b),
                            "style": "bold",
                            "fore": _branch_color,
                        },
                        {
                            "text": " <<< " if is_caller else "",
                            "style": "bold",
                            "fore": "yellow",
                        },
                        {
                            "text": "SOURCE" if is_caller else "",
                            "style": "bold",
                            "fore": "yellow",
                        },
                    ]
                )
            # if branches more than 3
            if len(_branch) > 4 and not is_caller:
                # print the lines branching off
                print_err(
                    [
                        {"text": "    at   ", "style": "bold", "fore": "black"},
                        {
                            "text": inter.shortened(_branch[0].strip()),
                            "style": "bold",
                            "fore": _branch_color,
                        },
                    ]
                )
                # print ...
                print_err(
                    [
                        {"text": "    at   ", "style": "bold", "fore": "black"},
                        {
                            "text": f"... ({len(_branch) - 4} more)",
                            "style": "bold",
                            "fore": "black",
                        },
                    ]
                )
            # if branches less than 3
            else:
                if len(_branch) > 7:
                    # print the before elipses
                    print_err(
                        [
                            {"text": "    at   ",
                                "style": "bold", "fore": "black"},
                            {
                                "text": f"... ({len(_branch) - MAX_SUBINSTRUCTIONS} more)",
                                "style": "bold",
                                "fore": "black",
                            },
                        ]
                    )
                    for i, _branch2 in enumerate(_branch[len(_branch) - MAX_SUBINSTRUCTIONS:]):
                        print_err(
                            [
                                {
                                    "text": "    at   ",
                                    "style": "bold",
                                    "fore": "black",
                                },
                                {
                                    "text": inter.shortened(_branch2.strip()),
                                    "style": "bold",
                                    "fore": _branch_color,
                                },
                            ]
                        )
                else:
                    for _branch2 in _branch[1:]:
                        print_err(
                            [
                                {
                                    "text": "    at   ",
                                    "style": "bold",
                                    "fore": "black",
                                },
                                {
                                    "text": inter.shortened(_branch2.strip()),
                                    "style": "bold",
                                    "fore": _branch_color,
                                },
                            ]
                        )
        # print the finishing divider
        print_err([{"text": divider, "style": "bold", "fore": "green"}])
        # print this error with print_err()
        print_err(
            [
                {"text": "[-] ", "style": "bold", "fore": "red"},
                {"text": err, "style": "bold", "fore": "red"},
                {"text": "\n"},
                {"text": msg, "style": "bold", "fore": "red"},
            ]
        )
        # add to log
        inter.log += f"{words_printed}\n"
    raise MSN2Exception("\n" +
                        bordered(
                            f"MSN2 Exception thrown, see above for details.\nError on line: {inst_tree[list(inst_tree.keys())[-1]][1]}\nError: {err}\n{msg}"))
