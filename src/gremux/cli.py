import logging
from gremux.cmds import sessionizer
import gremux.cmds.places as plc
import gremux.cmds.config as cfg
import gremux.struct as struct


def main():
    import argparse

    parser = argparse.ArgumentParser("gremux")
    sub = parser.add_subparsers(dest="cmd", required=False)

    # if nothign is provided, make the default to open something like
    # tmuxify to let the user choose something from a set of common locations
    # this common set might be useful to set up the first time and save on the config file?

    # parent flags
    source_parent = argparse.ArgumentParser(add_help=False)
    source_parent.add_argument(
        "--source",
        "-s",
        help="Source file",
    )

    # ================================
    # CONFIG FILE
    # ================================

    config = sub.add_parser("config")
    config_sub = config.add_subparsers(dest="config_cmd", required=True)

    config_up = config_sub.add_parser(
        "up", parents=[source_parent], help="Up a tmux session from a source file"
    )
    config_show = config_sub.add_parser(
        "show", parents=[source_parent], help="Create places.yml"
    )
    config_create = config_sub.add_parser(
        "create", parents=[source_parent], help="Create places.yml"
    )

    # ================================
    # PLACES FILE
    # ================================
    places = sub.add_parser("places")
    places_sub = places.add_subparsers(dest="places_cmd", required=True)

    places_create = places_sub.add_parser(
        "create", parents=[source_parent], help="Create places.yml"
    )

    places_create.add_argument(
        "--add",
        "-a",
        nargs="+",
        metavar="ITEM",
        help="Add to places.yml",
    )
    places_create.add_argument(
        "--maximum",
        "-m",
        type=int,
        help="Maximum amount of items in places.yaml",
    )

    args = parser.parse_args()
    logger = struct.get_logger(level=logging.INFO)

    if args.cmd == "config":
        if args.config_cmd == "up":
            cfg.up(args, logger)

        elif args.config_cmd == "show":
            cfg.show(args, logger)

        elif args.config_cmd == "create":
            cfg.create(args, logger)

    elif args.cmd == "places":
        if args.places_cmd == "create":
            plc.create(args, logger)

    else:
        sessionizer(logger)
