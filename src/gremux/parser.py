import yaml
from pathlib import Path
from gremux.grem import Grem
from gremux.context import Window, Pane, Layout


class Parser:
    def __init__(self, path: str = Path.cwd(), filename="grem.yaml"):
        self.path = path
        self.name = "grem.yaml"

        self.yaml = None

    def load(self) -> dict:
        path = Path(self.path).expanduser().resolve() / Path(self.name)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with path.open("r") as f:
            self.yaml = yaml.safe_load(f)

    def grem(self) -> Grem:
        if self.yaml is None:
            self.load()

        session = self.yaml["session"]
        # Note: i'll hardcode the session for now, since i might want to add multisession per project later?

        grem = Grem(name=session["name"])

        for cur_window in session["windows"]:
            window_obj = Window(cur_window["name"], Layout(cur_window["layout"]))

            for cur_pane in cur_window["panes"]:
                pane_obj = Pane(cur_pane["command"], cwd=None)
                window_obj.add_pane(pane_obj)

            grem.add_window(window_obj)

        return grem
