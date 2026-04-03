from dataclasses import dataclass, field
from typing import List
from enum import Enum

import os
import libtmux


class PlacesSource(Enum):
    ZOXIDE = "zoxide"
    DEFAULT = "default"
    BACKUP = "backup"
    NONE = None


class Layout(Enum):
    EVEN_HORIZONTAL = "even-horizontal"
    EVEN_VERTICAL = "even-vertical"
    MAIN_VERTICAL = "main-vertical"
    MAIN_HORIZONTAL = "main-horizontal"
    NONE = None


@dataclass
class Pane:
    """
    Base class for Pane configuration
    """

    command: list[str] | None = None
    cwd: str | None = None
    focus: bool = False
    env: dict[str, str] = field(default_factory=dict)


@dataclass
class Window:
    """
    Base class for Window Configuration
    """

    name: str
    layout: Layout
    panes: List[Pane] = field(default_factory=list)

    def add_pane(self, pane: Pane):
        """
        Add a pane to the Window
        """
        self.panes.append(pane)

    def to_dict(self) -> dict:
        panes = []
        for pane in self.panes:
            pane_data = {}

            if pane.cwd is not None:
                pane_data["cwd"] = pane.cwd

            pane_data["command"] = pane.command
            panes.append(pane_data)

        return {
            "name": self.name,
            "layout": self.layout.value,
            "panes": panes,
        }

    def apply(self, tmux_window: libtmux.Window, proj_dir: str):
        """
        Apply the current Window configuration to a tmux Window

        Parameters:
        ----------
        * `tmux_window`: libtimux.Window
        * `proj_dir`: str
        """

        # ===== LAYOUT ===== #
        layout = self.layout.value
        if layout is not None:
            tmux_window.select_layout(layout)

        # ===== SPLITS ===== #
        layout = self.layout.value
        num_panes = len(self.panes)
        for _ in range(num_panes - 1):
            tmux_window.split()

        # ===== PANE COMMANDS ===== #

        # - move to correct dir - #
        for prior_pane, tg_pane in zip(tmux_window.panes, self.panes):
            # set the working dir
            if tg_pane.cwd is None:
                prior_pane.send_keys(f"cd {proj_dir}", enter=True)
            else:
                tg_dir = os.path.join(proj_dir, tg_pane.cwd)
                prior_pane.send_keys(f"cd {tg_dir}", enter=True)

            # prior_pane.send_keys("clear", enter=True)

            # - send respective commands - #
            if tg_pane.command is not None:
                for cmd in tg_pane.command:
                    prior_pane.send_keys(cmd, enter=True)

            prior_pane.send_keys("clear", enter=True)

            # modify window width and all that

        # ===== MODIFY THE RELATIVE WIDTH/HEIGHT ===== #
        # wip
