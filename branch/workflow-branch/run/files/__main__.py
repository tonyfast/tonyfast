from typer import Typer, Context
from types import FunctionType
from importnb import Notebook
from importlib import import_module
from pathlib import Path

HERE = Path(__file__).parent

def get_commands():
    for line in (HERE/ "commands.txt").read_text().splitlines():
        right = line.lstrip()
        if right:
            if not right.startswith("#"):
                yield right.rstrip().split(maxsplit=1)

commands = list(get_commands())

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="rich",
    add_completion=False,
    no_args_is_help=True,
)


with Notebook():
    for name, ref in commands:
        module, _, ref = ref.rpartition(":")
        method = getattr(import_module(module, __package__), ref)
        if isinstance(method, FunctionType):
            app.command(name)(method)
        elif isinstance(method, Typer):
            app.registered_commands.extend(method.registered_commands)


if __name__ == "__main__":
    app()
