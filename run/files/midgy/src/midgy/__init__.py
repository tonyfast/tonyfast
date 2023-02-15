"""midgy translates (ie tangles) commonmark markdown to python code."""

__all__ = "Python", "md_to_python"
from .python import Python
from ._version import __version__

tangle = md_to_python = Python.code_from_string
