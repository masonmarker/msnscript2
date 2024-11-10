
from core.classes.var import Var


class Method:
        def __init__(self, name, interpreter):
            self.name = name
            self.args = []
            self.body = []
            self.returns = []
            self.ended = False
            self.interpreter = interpreter

        def add_arg(self, arg):
            self.args.append(arg)

        def add_body(self, body):
            self.body.append(body)

        def add_return(self, ret):
            self.returns.append(ret)

        # determines if the argument is a default value

        def default(self, func_insert, index):
            return isinstance(self.args[index], list) and func_insert is None

        # runs the method with the arguments passed

        def run(self, args, inter, actual_args=None):
            global lines_ran
            # finds an argument in the list of arguments
            def find_arg(func_var):
                ind = -1
                # for each arg in self.args
                for j, argname in enumerate(self.args):
                    # using default value
                    if isinstance(argname, list):
                        if argname[0] == func_var:
                            ind = j
                            break
                    # not
                    else:
                        if argname == func_var:
                            ind = j
                            break
                return ind

            # tries to place a variable in its argument location
            # before interpretation

            def try_var(func_var, func_insert):
                try:
                    # if self.args[i] is a list
                    if self.default(func_insert, i):
                        raise Exception()
                    # find the index of self.args
                    ind = find_arg(func_var)
                    if self.default(func_insert, ind):
                        inter.vars[func_var] = Var(self.args[ind][0], self.args[ind][1])
                    else:
                        inter.vars[func_var] = Var(func_var, func_insert)
                except Exception:
                    try:
                        if self.default(func_insert, i):
                            raise TypeError()
                        inter.vars[func_var] = func_insert
                    except TypeError:
                        # using default value
                        func_var, default_value = func_var
                        ind = find_arg(func_var)
                        if args[ind]:
                            inter.vars[func_var] = Var(func_var, args[ind])
                        elif default_value:
                            inter.vars[func_var] = Var(func_var, default_value)

            # loop through arguments to set
            for i in range(len(self.args)):
                if actual_args:
                    try:
                        if self.is_str(actual_args[i][0]):
                            try_var(self.args[i], args[i])
                            continue
                    # index out of bounds
                    except IndexError:
                        pass
                try:
                    inter.vars[self.args[i]] = inter.vars[args[i]]
                except:
                    try:
                        # print('func_var: ', self.args[i], 'func_insert: ', args[i], 'args: ', args)
                        try_var(self.args[i], args[i])
                        # print('stayed')
                    except IndexError:
                        # using default value
                        args.append(self.args[i][1])
                        try_var(self.args[i][0], args[i])
            # required number of arguments for this function
            # remove 'self' if this is a class function
            required_arg_num = len(self.args) - self.args.count("self")
            # adjust self.args to remove duplicate arguments
            # for each type list in self.args
            for lst in (
                with_list := [lst for lst in self.args if isinstance(lst, list)]
            ):
                # for each entry in the list
                for entry in lst:
                    # if the entry is in self.args
                    if entry in self.args:
                        # remove the entry
                        self.args.remove(entry)
            actual_arg_num = len(actual_args)
            for arg in actual_args:
                arg = arg[0]
                if arg == "":
                    actual_arg_num -= 1
            named_args_num = len(with_list)
            # check for error with named arguments
            if actual_arg_num + named_args_num < required_arg_num:
                inter.raise_incorrect_args(
                    required_arg_num,
                    actual_arg_num + named_args_num,
                    self.body[0],
                    lines_ran,
                    self,
                )
            for line in self.body:
                method_ret = inter.interpret(line)
            return method_ret

        def is_str(self, value):
            return (value[0] == '"' and value[-1] == '"') or (
                value[0] == "'" and value[-1] == "'"
            )
