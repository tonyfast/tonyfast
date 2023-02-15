from importlib import import_module
from functools import partial
imports = partial(import_module, package=__package__)
with __import__("importnb").Notebook():
    MarkdownNotebook = imports(".xxii.2022-12-23-mkdocs-plugin").MarkdownNotebook