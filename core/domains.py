
def f_domain(inter, line, args, **kwargs):
    # get the name of the domain to create
    domain_name = inter.parse(0, line, args)[2]
    # domain_name must be a varname
    inter.check_varname(domain_name, line)
    # domains cannot coexist
    if domain_name in inter.domains:
        inter.err(
            "Domain Error",
            f'Domain "{domain_name}" already exists',
            line,
            kwargs["lines_ran"],
        )
    # add the domain_name to the set
    inter.domains.add(domain_name)
    # interpret the block in a new interpreter
    # with the domain_name as the parent
    new_int = inter.new_int()
    new_int.execute(args[1][0])
    # throws a domain error

    def domain_err(name, object):
        inter.err(
            "Domain Error",
            f'Domain object name already claimed: "{name}", consider renaming the object',
            line,
            kwargs["lines_ran"],
        )
        
    # for each variable in the interpreter
    for varname in new_int.vars:
        name = f"{domain_name}:{varname}"
        # name cannot already exist
        if name in inter.vars:
            domain_err(name, inter.vars)
        inter.vars[name] = new_int.vars[varname]
    # do the same for methods
    for methodname in new_int.methods:
        name = f"{domain_name}:{methodname}"
        if name in inter.methods:
            domain_err(name, inter.methods)
        inter.methods[name] = new_int.methods[methodname]
    return domain_name
def d_domainfind(inter, line, args, **kwargs):
    # get the domain directory
    domain_dir = inter.parse(0, line, args)[2]
    # domain_dir must be a varname
    inter.check_varname(domain_dir, line)
    # get all variables in the domain
    # with the domain_dir chopped off
    domain_vars = {}
    # for each variable in the domain
    for varname in inter.vars:
        # if the variable is in the domain
        if varname.startswith(domain_dir):
            # get the variable name without the domain
            varname = varname[len(domain_dir):]
            # add the variable to the domain_vars
            domain_vars[varname] = inter.vars[varname]
    # return the domain_vars
    return domain_vars


DOMAINS_DISPATCH = {
    "domain": f_domain,
    "domain:find": d_domainfind,
}