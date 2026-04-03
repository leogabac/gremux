# ==============================================================================
# This file makes a rough implementation of tmux-sessionizer
# ==============================================================================

from pathlib import Path
from itertools import chain
import libtmux

from gremux.core import get_places, fzf_select
import gremux.struct as gst


def sessionizer(logger):
    """
    tmux sessionizer
    Inspired by ThePrimeagen's tool
    https://github.com/ThePrimeagen/tmux-sessionizer

    When invoked, opens a fzf with all your common locations set up at
    ~/.config/gremux/places.yml

    Then opens a tmux session set up with the local grem.yaml file
    If there is not, then it opens a default setup
    """

    # get the common places and select the project directoy
    common_dirs = get_places()
    if common_dirs is None:
        message = [
            "places.yml is not configred! Run.",
            "gremux places create -s SOURCE",
            "Exiting",
        ]
        logger.info("\n".join(message))

        return None

    places = [Path(d).expanduser() for d in common_dirs]

    dirs = [
        str(p)
        for p in chain.from_iterable(r.iterdir() for r in places if r.is_dir())
        if p.is_dir()
    ]

    selection = fzf_select(logger, dirs)

    if not selection:
        logger.info("No directory selected, exiting...")
        return

    # connect to a tmux server

    server = libtmux.Server()

    proj_dir: str = selection

    # Sessionizer is responsible for project selection only.
    # Session creation/attachment belongs to the Grem model so that
    # `gremux` and `gremux config up` share the same launch path.
    parser = gst.Parser(proj_dir)
    cfg: gst.Grem = parser.grem()

    cfg.launch(server, proj_dir)

    return None
