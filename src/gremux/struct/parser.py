import yaml
from pathlib import Path
from gremux.struct.grem import Grem
from gremux.struct.context import Window, Pane, Layout


class Parser:
    def __init__(self, path: Path | str = Path.cwd(), filename="grem.yaml"):
        self.path = path
        self.name = filename
        self.gremfile = Path(self.path).expanduser().resolve() / Path(self.name)

        self.yaml = None

    def load(self) -> dict:
        # path = Path(self.path).expanduser().resolve() / Path(self.name)

        if not self.gremfile.exists():
            raise NotADirectoryError("grem.yaml not found. Exiting...")

        with self.gremfile.open("r") as f:
            self.yaml = yaml.safe_load(f)

    def _default_grem(self) -> Grem:
        panes = [Pane(command=None, cwd=None)]
        windows = [Window(name="default", layout=Layout(None), panes=panes)]
        grem = Grem(name=Path(self.path).name, windows=windows)

        return grem

    def grem(self) -> Grem:
        # if there is no project gremfile
        # then make a default configuration
        if not self.gremfile.exists():
            return self._default_grem()

        if self.yaml is None:
            self.load()

        session = self.yaml["session"]
        # Note: i'll hardcode the session for now, since i might want to add multisession per project later?

        grem = Grem(name=session["name"])

        for cur_window in session["windows"]:
            layout_value = cur_window.get("layout", None)
            window_obj = Window(cur_window["name"], Layout(layout_value))

            for cur_pane in cur_window["panes"]:
                pane_obj = Pane(cur_pane["command"], cwd=cur_pane["cwd"])
                window_obj.add_pane(pane_obj)

            grem.add_window(window_obj)

        return grem
