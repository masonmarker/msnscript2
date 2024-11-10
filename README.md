
# PULLING FROM GITHUB

when pulling from GitHub, you should thoroughly review the version changes in both the commit history, and ```/system/changes.json``` to ensure that your existing code is compatible with the latest version of the msn2 library. commits are made often, and this only emphasizes the importance of reviewing the changes made to the library.

## setup

*It's heavily suggested to install the msn2-syntax-highlighter package for your text editor to make coding in msn2 easier.*

the insertion ```{python_alias}``` specified below is your machine's python alias.
for most this is 'python', however it may be different for you.
if yours is different, you should set your python alias under msn2_settings.json that should be created in your ```msnscript2/``` directory after an initial launch of a .msn2 program.

### installing dependencies

while globally installing dependencies isn't recommended, you can do this with ```{python_alias} msn2cli.py install```

not all dependencies might be used in your programs, so it's recommended to install dependencies as needed.

these dependencies can also be re-installed via the msn2 help pages if necessary
as of 2.0.385. find these pages and much more with ```{python_alias} msn2cli.py help```

### starting a .msn2 script (latest version, recommended)

1. ```cd msnscript2```
2. ```{python_alias} msn2cli.py -f script1```

the ```.msn2``` file extension is optional when specifying a file to execute.

#### CLI examples

##### multiple files

- ```{python_alias} msn2cli.py -f script1 -f script2```

##### multiple files with system arguments

- ```{python_alias} msn2cli.py time -f script1 -a "['hello', 'bye']" -f script2 -a "'no way'"```

##### running just a code snippet

- ```{python_alias} msn2cli.py -s "(@v = 1, print(v))"``` -> "1"

##### timing .msn2 code

- ```{python_alias} msn2cli.py time -s "sleep(1)"```

run ```{python_alias} msn2cli.py --help``` for more information on the msn2cli interpreter and its usage.

### starting a .msn2 script (pre 2.0.401)

    - you should run programs from /msnscript2

       if it works you can use: $ msn2 script.msn2 script2.msn2
       else: $ {python_alias} msn2.py script.msn2 script2.msn2

       the in() call retrieves arguments to the command line
       in the msn2 environment

    see the msn2 help pages via ```{python_alias} msn2.py help``` too see the most updated syntax and usage.
    see /TUTORIAL for the msn2 source code for this demonstration.
    other syntax likely exists outside of the suggested syntax, however outside syntax works in very
    specific scenarios, and are not recommended to be used. 

    the suggested syntax is the most updated, and safest way to code.

### known issues

find language integrity related issues under the issues tab of this repository.

### notes

- see /demos for demonstrations
- see /tests for syntax specific usage (find the most recent validator in /tests)
- see /projects for larger demonstrations
- see /msn2 for a portable MSNScript2 Interpreter package that can be copied
    into your project directories for launching .msn2 programs anywhere.
- see /problems for popular programming problems solved in msn2.
- see /system for system related operations in msn2.

- run ```{python_alias} msn2cli.py verify``` to run the validator for msn2 integrity.

- file-based code depends on the user's current directory after executing a .msn2 program (ex imports),
- verify that file paths in written code are compatible with the directory at which the program is launched

- be wary of function name changes in the msn2 library, the libraries and interpreter are subject to change,
this is to make the library safer and/or faster. be sure to read commits of TheMsnProject
to understand the status and naming conventions of the latest versions of the package.

again, run '{python_alias} msn2.py help' for more information on the msn2 interpreter and its usage,
or see more help through the CLI with ```{python_alias} msn2cli.py --help```
