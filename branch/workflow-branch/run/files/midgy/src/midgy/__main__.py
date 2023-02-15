from argparse import ArgumentParser
from pathlib import Path

from .loader import Markdown

parser = ArgumentParser("midgy", description="run markdown files")
sub = parser.add_subparsers(dest="subparser")
run = sub.add_parser("run")
run = Markdown.get_argparser(run)
run.add_argument(
    "--doctest-is-code",
    action="store_true",
    help="include doctest input in code generation.",
    dest="include_doctest",
)
convert = sub.add_parser("convert")

subs = {"run", "convert"}
try:
    # set up rich
    from rich import print
    from rich.traceback import install

    install(suppress=[])
except ModuleNotFoundError:
    pass


def main(parser=parser):
    from sys import argv

    Markdown.load_argv(argv[1:])


if __name__ == "__main__":
    main()
