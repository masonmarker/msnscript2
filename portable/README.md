# portable MSN2 Directories

1. create a fresh, lightweight yet all-inclusive MSN2 package that can be copied to any of your projects:

```sh
{python_alias} msn2cli.py portable
```

this will create a folder called `msn2/` within this `portable/` directory that contains all the necessary files to run MSN2 code in any location.

2. copy the `msn2/` folder to your project directory
3. inside of the `msn2/` folder, create a new .msn2 file
4. in your project directory, you or a process should run:

```sh
cd msn2
```

and a following msn2 execution command such as:

```sh
{python_alias} msn2cli.py -f <your_msn2_file>
```

dependencies for the msn2 runner are not automatically installed within the pasting location, so you will need to install then yourself, or globally through the help pages:

```sh
{python_alias} msn2cli.py help
```

Happy... what was it... hexing?...humming?... no, hacking! Happy hacking!
