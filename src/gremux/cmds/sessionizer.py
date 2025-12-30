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
    dir_name = Path(proj_dir).name

    # pass to the parser
    parser = gst.Parser(proj_dir)
    cfg: gst.Grem = parser.grem()

    # start the session with my 0th window
    match_session = server.sessions.filter(session_name=cfg.name)
    if len(match_session) > 0:
        match_session[0].attach(exit_=True)
        return None

    session = server.new_session(
        session_name=cfg.name,
        kill_session=True,  # replace if it already exists
        attach=False,
        window_name=cfg.windows[0].name,
        start_directory=proj_dir,
    )

    # setup and create rest of the windows
    for i, cfg_window in enumerate(cfg.windows):
        if i == 0:
            tmux_window = session.windows[0]
        else:
            tmux_window = session.new_window(window_name=cfg_window.name)

        cfg_window.apply(tmux_window, proj_dir)

    session.attach(exit_=True)

    return None
