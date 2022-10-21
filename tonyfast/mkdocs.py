import os
from pathlib import Path
from shlex import split
from subprocess import check_call, check_output
from mkdocs.plugins import BasePlugin

class HatchLite(BasePlugin):
    def on_post_build(self, config, **kwargs):
        target = Path(config["site_dir"]) / "run"
        if "tmp" not in target.as_posix():
            check_call(split( F"jupyter lite build --contents tonyfast --output-dir {target.as_posix()}"))