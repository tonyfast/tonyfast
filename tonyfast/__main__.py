from typer import Typer
from types import FunctionType
from importnb import Notebook
from importlib import import_module

commands = [
    "hello .xxii.2022-12-19-integrating-typer:main".split(),
]

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


if __name__ == "__main__":
    app()
