import logging
from pathlib import Path
import gremux.struct as gst
import libtmux


def up(args, logger):
    if args.source is None:
        args.source = Path.cwd()

    up_source(args, logger)
    return


def up_source(args, logger):
    parser = gst.Parser(args.source)
    cfg: gst.Grem = parser.grem()

    # connect to a tmux server

    server = libtmux.Server()

    cfg.launch(server, args.source)

    return None


def show(args, logger):
    print(args)
    return


def create(args, logger):
    print(args)
    return
