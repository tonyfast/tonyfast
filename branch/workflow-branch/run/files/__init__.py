try:
    from midgy.loader import Markdown
except ModuleNotFoundError:
    from midgy.run import Markdown

with Markdown():
    from . import *

APPNAME = "tonyfast"


def get_requests_cache(name=APPNAME):
    from requests_cache import install_cache

    install_cache(APPNAME, backend="filesystem", use_cache_dir=True)

def load_ipython_extension(shell):
    pass

def unload_ipython_extension(shell):
    pass

import importnb    
with importnb.Notebook():
    from . import regexs