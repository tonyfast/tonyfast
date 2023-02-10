__all__ = "Python", "md_to_python"
from .python import Python

tangle = md_to_python = Python.code_from_string
