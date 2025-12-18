from dataclasses import dataclass, field
from typing import List
from gremux.struct.context import Window
import libtmux


@dataclass
class Grem:
    """
    Base class for the configuration file.
    """

    name: str
    windows: List[Window] = field(default_factory=list)

    def add_window(self, window: Window):
        """Add a Window to the configuration file"""
        self.windows.append(window)

    def launch(self, server: libtmux.Server, proj_dir):
        """
        Launch a tmux session with the current configuration

        Parameters:
        * `server`: libtimux.Server
        * `proj_dir`: str
        """
        # start the session with my 0th window
        match_session = server.sessions.filter(session_name=self.name)
        if len(match_session) > 0:
            match_session[0].attach(exit_=True)
            return None

        session = server.new_session(
            session_name=self.name,
            kill_session=True,  # replace if it already exists
            attach=False,
            window_name=self.windows[0].name,
            start_directory=proj_dir,
        )

        # setup and create rest of the windows
        for i, cfg_window in enumerate(self.windows):
            if i == 0:
                tmux_window = session.windows[0]
            else:
                tmux_window = session.new_window(window_name=cfg_window.name)

            cfg_window.apply(tmux_window, proj_dir)

        session.attach(exit_=True)

        return
