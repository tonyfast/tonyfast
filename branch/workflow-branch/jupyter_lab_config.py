if "c" not in locals():
    from traitlets.config import Config
    c = Config()
    
import datetime

c.ContentsManager.untitled_notebook = (
    c.ContentsManager.untitled_file
) = f"{datetime.date.today():%Y-%m-%d}-"

c.ContentsManager.hide_globs = []
c.JupyterApp.open_browser = False
c.JupyterApp.log_level = 0

c.VideoChat.update(
    {
        "room_prefix": "litprog-writers-workshop",
        "rooms": [
            {
                "id": "bounce-house",
                "displayName": "where the party is at",
                "description": "writers workshop class room",
            }
        ],
    }
)

# c.LabApp.collaborative = True

c["@deathbeds/jupyterlab-fonts:fonts"].styles = {
    "@import": [
        "https://tools-static.wmflabs.org/fontcdn/css?family=Libre+Baskerville:400,400italic,700&subset=latin,latin-ext"
    ],
    ":root": {
        "--jp-code-font-family": "'Fira Code Medium', var(--jp-code-font-family-default)",
        "--jp-content-font-family": "'Libre Baskerville', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'",
        "--jp-border-color0": "transparent",
        "--jp-border-color1": "transparent",
        "--jp-border-color2": "transparent",
        "--jp-cell-editor-border-color": "transparent",
        "--jp-toolbar-border-color": "transparent",
    },
}