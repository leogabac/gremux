from dataclasses import dataclass, field
from typing import List
from gremux.context import Window


@dataclass
class Grem:
    """
    Base class for the configuration file.
    """

    name: str
    windows: List[Window] = field(default_factory=list)

    def add_window(self, window: Window):
        self.windows.append(window)
