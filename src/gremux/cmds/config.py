import logging
from pathlib import Path
import gremux.struct as gst
import libtmux
import os
import yaml


def _config_dir() -> Path:
    return Path.home() / ".config" / "gremux"


def up(args, logger) -> None:
    if args.source is None:
        args.source = Path.cwd()

    up_source(args, logger)
    return None


def up_source(args, logger) -> None:
    parser = gst.Parser(args.source)
    cfg: gst.Grem = parser.grem()

    try:
        server = libtmux.Server()
        cfg.launch(server, parser.path)
    except libtmux.exc.LibTmuxException as exc:
        logger.error(f"tmux is unavailable or returned an error: {exc}")
        return None

    return None


def show(args, logger) -> None:
    if args.source is None:
        args.source = Path.cwd()

    show_source(args, logger)
    return


def show_source(args, logger) -> None:
    parser = gst.Parser(args.source)
    cfg: gst.Grem = parser.grem()

    if parser.loaded_from is None:
        logger.info("Resolved config source: in-memory default")
    else:
        logger.info(f"Resolved config source: {parser.loaded_from}")

    print(yaml.safe_dump(cfg.to_dict(), sort_keys=False).rstrip())

    return None


def create(args, logger) -> None:
    if args.source is None:
        logger.info("Must provide the --source argument")
        return None

    create_source(args, logger)

    return None


def create_source(args, logger) -> None:
    if args.source == "default":
        config_dir = _config_dir()
        config_dir.mkdir(parents=True, exist_ok=True)
        default_file = config_dir / "default.yaml"

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

        with default_file.open("w") as fh:
            yaml.safe_dump(default, fh)

        logger.info(f"Written to {default_file}")
    else:
        logger.info("Feature not available. Exiting.")

    return None
