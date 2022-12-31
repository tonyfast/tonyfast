if "c" not in locals():
    from traitlets.config import Config
    c = Config()

c.InteractiveShellApp.extensions = [
    "tonyfast"
]
c.InteractiveShellApp.exec_lines = [
    'locals().setdefault("__path__", ["."])',
]