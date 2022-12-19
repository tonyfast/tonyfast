try:
    from midgy.loader import Markdown
except ModuleNotFoundError:
    from midgy.run import Markdown

with Markdown():
    from . import *