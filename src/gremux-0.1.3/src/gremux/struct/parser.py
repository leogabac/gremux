import yaml
from pathlib import Path
from gremux.struct.grem import Grem
from gremux.struct.context import Window, Pane, Layout


class Parser:
    """
    Base parser class
    """

    def __init__(self, path: Path | str = Path.cwd(), filename="grem.yaml"):
        source = Path(path).expanduser()

        if source.name == filename or source.suffix in {".yaml", ".yml"}:
            self.path = source.parent.resolve()
            self.name = source.name
            self.gremfile = source.resolve()
        else:
            self.path = source.resolve()
            self.name = filename
            self.gremfile = self.path / Path(self.name)

        self.yaml = None
        self.session_name = None
        self.loaded_from: Path | None = None

    def load(self) -> dict:
        """
        Load a grem.yaml file
        """

        if not self.gremfile.exists():
            raise NotADirectoryError("grem.yaml not found. Exiting...")

        with self.gremfile.open("r") as f:
            self.yaml = yaml.safe_load(f)
        self.loaded_from = self.gremfile

    def _default_grem(self) -> Grem:
        """
        Set the default to open in case there is no grem.yaml in the project's root.
        """
        panes = [Pane(command=None, cwd=None)]
        windows = [Window(name="default", layout=Layout(None), panes=panes)]
        grem = Grem(name=Path(self.path).name, windows=windows)
        self.loaded_from = None

        return grem

    def _normalize_command(self, command) -> list[str] | None:
        """
        Normalize pane commands into the internal list form.
        """

        if command is None:
            return None

        if isinstance(command, str):
            return [command]

        if isinstance(command, list):
            return [item for item in command if item is not None]

        raise TypeError("pane.command must be a string, a list, or null")

    def grem(self) -> Grem:
        """
        From a given grem.yaml file, convert it into a configuration Grem object
        """

        # If there is no local grem.yaml, goes to default.yaml
        # If there is none, then it goes to a default thing still.

        if not self.gremfile.exists():
            config_path = Path.home() / ".config" / "gremux"
            filename = Path("default.yaml")
            default_gremfile = config_path / filename

            # If we're already trying the default, stop recursing
            if self.gremfile.resolve() == default_gremfile.resolve():
                return self._default_grem()

            # Otherwise, switch to default and try again
            self.session_name = Path(self.path).name
            self.name = filename
            self.gremfile = default_gremfile.expanduser().resolve()

            return self.grem()  # IMPORTANT: return it

        if self.yaml is None:
            self.load()

        session = self.yaml["session"]
        # Note: i'll hardcode the session for now, since i might want to add multisession per project later?

        # This triggers only when there is no grem.yaml file
        # as self.session_name is kept at None
        if self.session_name is None:
            self.session_name = session["name"]

        grem = Grem(name=self.session_name)

        for cur_window in session["windows"]:
            layout_value = cur_window.get("layout", None)
            window_obj = Window(cur_window["name"], Layout(layout_value))

            for cur_pane in cur_window["panes"]:
                pane_obj = Pane(
                    command=self._normalize_command(cur_pane.get("command")),
                    cwd=cur_pane.get("cwd"),
                )
                window_obj.add_pane(pane_obj)

            grem.add_window(window_obj)

        return grem
