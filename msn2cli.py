"""Command line interface entry point for MSN2."""

# CLI
import click

# msn2 execution
from msn2python import run
from msnint2 import Interpreter


@click.command(help=".msn2 file runner and interpreter",
               epilog="Find more documentation at https://www.masonmarker.com/projects/msn2")
@click.argument("action", type=str, default="run")
# click argument for the file, can be --file or -f
@click.option("--file", "-f", type=str, multiple=True,
              help="The path to a .msn2 file to run (.msn2 is not required)")
# sys args to msn2
@click.option("--args", "-a", type=str, multiple=True,
              help="The arguments to pass to a respective .msn2 file")
# runs an msn2 snippet
@click.option("--snippet", "-s", type=str, multiple=True,
              help="An msn2 code snippet to run")
def main(action, file, args, snippet):
    
    
    """Main entry point for the CLI."""
    def _run(f, args, i):
        run(f, args[i] if args and i < len(args) else None)

    def _fix_file(f):
        return f if f.endswith(".msn2") else f + ".msn2"

    def _run_snippets(i: Interpreter):
        for s in snippet:
            i.interpret(s)
    # requires that a file or snippet was provided
    def _require_file_or_snippet():
        if len(file) == 0 and len(snippet) == 0:
            i = Interpreter()
            # error that no files were provided
            i.styled_print([
                {"text": "[", "fore": "black"},
                {"text": "MSN2", "fore": "yellow"},
                {"text": "] ", "fore": "black"},
                {"text": "No files or snippets provided", "fore": "red"}
            ])
            exit()
    # collect actions
    def _actions():
        # create action functions
        def __run():
            _require_file_or_snippet()
            for i, f in enumerate(file):
                _run(_fix_file(f), args, i)
            _run_snippets(Interpreter())
        def __time():
            import time

            _require_file_or_snippet()
            i = Interpreter()
            def _timed_function(func, f):
                i.styled_print([{"text": "-" * 20, "fore": "black"}])
                i.styled_print(
                    [{"text": f"Starting timed program: {f}", "fore": "blue"}])
                start = time.time()
                func()
                end = time.time()
                i.styled_print(
                    [{"text": f"Finished in: {end - start} seconds", "fore": "green"}])
                i.styled_print([{"text": "-" * 20, "fore": "black"}])
            for f in file:
                _timed_function(lambda: run(
                    _fix_file(f), args[0] if args else None), f)
            i = Interpreter()
            _timed_function(lambda: _run_snippets(i), "")
        def _install_deps():
            import os
            os.system("pip install -r requirements.txt")
        return {
            "run": __run,
            "time": __time,
            "verify": lambda: run('tests/validator.msn2'),
            "portable": lambda: run('portable/port.msn2'),
            "test": lambda: run('tests/misc.msn2'),
            "int": lambda: run('system/int.msn2'),
            "file": lambda: run('system/file.msn2'),
            "help": lambda: run('TUTORIAL/driver.msn2'),
            "elements": lambda: run('tests/2.0.3x/practical/auto/clicked.msn2'),
            "install": _install_deps
        }
    cli_dispatch = _actions()
    if action in cli_dispatch:
        cli_dispatch[action]()
    else:
        # create an interpreter for printing
        i = Interpreter()
        # action not found error
        i.styled_print([
            {"text": "[", "fore": "black"},
            {"text": "MSN2", "fore": "yellow"},
            {"text": "] ", "fore": "black"},
            {"text": f"Action not found: {action}", "fore": "red"},
        ]),
        i.styled_print([
            {"text": "[", "fore": "black"},
            {"text": "MSN2", "fore": "yellow"},
            {"text": "] ", "fore": "black"},
            {"text": "Available actions: ", "fore": "white"},
            {"text": ", ".join(list(cli_dispatch.keys())), "fore": "green"}
        ])
        # see '--help' for more
        i.styled_print([
            {"text": "[", "fore": "black"},
            {"text": "MSN2", "fore": "yellow"},
            {"text": "] ", "fore": "black"},
            {"text": "See '--help' for more", "fore": "white"}
        ])
        exit()


if __name__ == "__main__":
    main()
