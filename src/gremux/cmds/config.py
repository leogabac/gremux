import logging
from pathlib import Path
import gremux.struct as gst
import libtmux
import os
import yaml


def up(args, logger) -> None:
    if args.source is None:
        args.source = Path.cwd()

    up_source(args, logger)
    return None


def up_source(args, logger) -> None:
    parser = gst.Parser(args.source)
    cfg: gst.Grem = parser.grem()

    # connect to a tmux server

    server = libtmux.Server()

    cfg.launch(server, args.source)

    return None


def show(args, logger) -> None:
    if args.source is None:
        args.source = Path.cwd() / Path("grem.yaml")

    show_source(args, logger)
    return


def show_source(args, logger) -> None:
    if not Path(args.source).exists():
        logger.info("grem.yaml was not found. Exiting.")
        return

    with open(args.source) as fh:
        for line in fh:
            print(line.rstrip())

    return None


def create(args, logger) -> None:
    if args.source is None:
        logger.info("Must provide the --source argument")
        return None

    create_source(args, logger)

    return None


def create_source(args, logger) -> None:
    if args.source == "default":
        home_dir = os.environ.get("HOME")
        default_file = os.path.join(home_dir, ".config", "gremux", "default.yaml")

        default = {
            "session": {
                "name": "default",
                "windows": [
                    {
                        # ide
                        "name": "0",
                        "layout": None,
                        "panes": [
                            {
                                "cwd": ".",
                                "command": [None],
                            }
                        ],
                    },
                ],
            }
        }

        with open(default_file, "w") as fh:
            yaml.safe_dump(default, fh)

        logger.info(f"Written to {default_file}")
    else:
        logger.info("Feature not available. Exiting.")

    return None
