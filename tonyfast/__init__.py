from midgy.run import Markdown

with Markdown():
    from . import README

with __import__("importnb").Notebook(lazy=True):
    from . import _022_10_05_dask_search as search
