from dataclasses import dataclass, field
from typing import List
from enum import Enum


class Layout(Enum):
    EVEN_HORIZONTAL = "even-horizontal"
    EVEN_VERTICAL = "even-vertical"
    MAIN_VERTICAL = "main-vertical"


@dataclass
class Pane:
    """
    Base class for whatever is inside a pane
    """

    command: str
    cwd: str | None = None
    focus: bool = False
    env: dict[str, str] = field(default_factory=dict)


@dataclass
class Window:
    """
    Base class for whatever is inside a window based on the configuration file.
    """

    name: str
    layout: Layout
    panes: List[Pane] = field(default_factory=list)

    def add_pane(self, pane: Pane):
        self.panes.append(pane)
