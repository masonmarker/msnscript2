![image](https://github.com/user-attachments/assets/f1a5b992-ac77-4304-90e3-9d4f53d91000)
<sub>*unformatted, runnable code, see below for more code examples*</sub>


# 🚀 msnscript2 (msn2)

[![Project Version][version-image]][version-url]
[![Backend][backend-image]][backend-url]
[![Minimum Python Version][minimum-python]][repository-url]
[![Documentation][docs-image]][docs-url]
[![SyntaxHighlighting][syntax-highlighting]][syntax-highlighting-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Website][website-shield]][website-url]

## ❗ PULLING NEW CHANGES ❗

when pulling new changes after already having cloned, you should thoroughly review the version changes in both the commit history, and `/system/changes.json` to ensure that your existing code is compatible with the latest version of the msn2 library. commits are made often, and this only emphasizes the importance of reviewing the changes made to the language.

---

### 📋 steps after cloning

1. navigate to the cloned repository:

```sh
cd msnscript2
```

2. install dependencies in `requirements.txt`, this can be done through pip or globally with:

```sh
{python_alias} msn2cli.py install
```

3. launch the msn2 help pages with:

```sh
{python_alias} msn2cli.py help
```

4. navigate to the _settings_ page

5. set your python _runner_alias_ (for most this is set to 'python'). specifying this is important for calls such as proc() or JAVA().

6. ensure your alias has been set correctly, and the integrity of the msn2 library is intact with:

```sh
{python_alias} msn2cli.py verify
```

7. install the [msn2-syntax-highlighting](https://marketplace.visualstudio.com/items?itemName=MasonMarker.msn2-syntax-highlighting) VS Code extension (or use the _CoffeeScript_ language mode if this isn't available to you)

8. learn to code in msn2 by reading through and running `TUTORIAL/suggestedusage2.msn2` as well as files in `demos/`, `problems/`, and `projects/`

---

### ⚡ starting a .msn2 script (latest version, recommended)

create a file with a `.msn2` extension in the `msnscript2/` directory to get started 🚀

there are a few ways to launch an msn2 program, but the recommended way uses the msn2 CLI:

```sh
cd msnscript2
```

```sh
{python_alias} msn2cli.py -f script1
```

you should be in the `msnscript2/` directory when launching programs or interacting with the msn2 CLI.

the `.msn2` file extension is optional when specifying a file to execute.

#### CLI examples

multiple files:

```sh
{python_alias} msn2cli.py -f script1 -f script2
```

<!--
##### multiple files with system arguments

- `{python_alias} msn2cli.py time -f script1 -a "['hello', 'bye']" -f script2 -a "'no way'"` -->

multiple files with system arguments:

```sh
{python_alias} msn2cli.py time -f script1 -a "['hello', 'bye']" -f script2 -a "'no way'"
```

running just a code snippet:

```sh
{python_alias} msn2cli.py -s "(@v = 1, print(v))"
```

timing .msn2 code:

```sh
{python_alias} msn2cli.py time -s "sleep(1)"
```

run `{python_alias} msn2cli.py --help` for more information on the msn2cli interpreter and its usage.

---

### 💻 code examples
let's take a glance at some msn2 code...

*basic variables and functions*

![image](https://github.com/user-attachments/assets/f1932e0a-7a80-49fb-a599-6c5ff1ac8984)

*starting an API endpoint and querying*

![image](https://github.com/user-attachments/assets/3cddfd61-c2ec-4971-a5c2-314278ed7e41)

*custom syntax*

![image](https://github.com/user-attachments/assets/cdbb0ffe-2d83-46ec-b7d8-df15b4205276)

*inline foreign languages*
*AS OF 2.0.403: JAVA(), JS(), C()*

![image](https://github.com/user-attachments/assets/7d12a698-0d12-45e4-99c7-db3f98d08b18)

*inline Python*

![image](https://github.com/user-attachments/assets/b8ba6317-cf16-4af3-b759-e81d30da7326)

*automates Cookie Clicker online!*

![image](https://github.com/user-attachments/assets/9afec34b-9a57-4821-a82f-e7bdc37b5685)

There's so much more here to uncover aside from the above examples, I'm actually getting giddy just explaining the possibilities, see the below `tutorials` section for more focused teachings.

---

### 👩🏼‍🏫 tutorials

See the msn2 suggested usage and tutorials in the `TUTORIAL/` directory for more information on how to use the msn2 language.

The help pages also offer a walkthrough of the suggested usage, invoke the help pages with:

```sh
{python_alias} msn2cli.py help
```

---

### ❗ known issues 

as much as I wish there weren't bugs in such a large, overly complex, single contributor having repository, there are XD.


find the dreaded language integrity related issues under the [issues](https://github.com/masonmarker/msnscript2/issues) tab of this repository.

---

### 📝 notes

- see `demos/` for demonstrations
- see `problems/` for popular programming problems solved in msn2.
- see `projects/` for larger, multi-filed demonstrations
- see the README in `portable/` for a smaller, lightweight msn2 interpreter package that can be copied anywhere as a portable msn2 runner in your projects.
- see `system/` for system related operations in msn2.
- see `tests/` for syntax specific usage (find the most recent validator in /tests)

*run `{python_alias} msn2.py help` for more information on the msn2 interpreter and its usage, and see more help with the CLI with `{python_alias} msn2cli.py --help`*

---

## Contributing

1. Fork it (<https://github.com/masonmarker/msnscript2/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

[repository-url]: https://github.com/masonmarker/msnscript2
[linkedin-url]: https://www.linkedin.com/in/masonmarker
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[website-url]: https://masonmarker.com
[website-shield]: https://img.shields.io/badge/-portfolio-black.svg?style=for-the-badge&logo=Google-Chrome&colorB=555
[docs-url]: https://masonmarker.com/projects/msn2
[docs-image]: https://img.shields.io/badge/Docs-msn2<=2.0.401-blue?style=for-the-badge&logo=appveyor
[version-image]: https://img.shields.io/badge/Version-2.0.403-brightgreen?style=for-the-badge&logo=appveyor
[version-url]: https://img.shields.io/badge/version-1.0.0-green
[backend-image]: https://img.shields.io/badge/Backend-Python-blue?style=for-the-badge
[backend-url]: https://img.shields.io/badge/Backend-Python-blue?style=for-the-badge
[minimum-python]: https://img.shields.io/badge/Requires%20Python-3.8%2B-blue?style=for-the-badge
[syntax-highlighting]: https://img.shields.io/badge/Syntax%20Highlighting-%20VSCode%20Marketplace-orange?style=for-the-badge
[syntax-highlighting-url]: https://marketplace.visualstudio.com/items?itemName=MasonMarker.msn2-syntax-highlighting
