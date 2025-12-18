import logging
from gremux.cmds import sessionizer
import gremux.cmds.places as plc
import gremux.cmds.config as cfg
import gremux.struct as struct


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="gremux",
        description=(
            "Declarative tmux session manager.\n\n"
            "If run without any arguments, gremux launches the interactive "
            "sessionizer to select a project and attach to a tmux session."
        ),
    )

    sub = parser.add_subparsers(
        dest="cmd",
        metavar="<command>",
    )

    # ================================
    # Shared parent arguments
    # ================================
    source_parent = argparse.ArgumentParser(add_help=False)
    source_parent.add_argument(
        "--source",
        "-s",
        metavar="PATH",
        help=("Source file or directory.\nDefaults to the current working directory."),
    )

    # ================================
    # CONFIG COMMANDS
    # ================================
    config = sub.add_parser(
        "config",
        help="Manage gremux session configuration files",
        description=(
            "Commands for creating, inspecting, and launching tmux sessions "
            "from grem.yaml configuration files."
        ),
    )
    config_sub = config.add_subparsers(
        dest="config_cmd",
        metavar="<subcommand>",
        required=True,
    )

    config_sub.add_parser(
        "up",
        parents=[source_parent],
        help="Launch a tmux session from a grem.yaml file",
        description=(
            "Parse a grem.yaml configuration file and launch or attach to "
            "the corresponding tmux session."
        ),
    )

    config_sub.add_parser(
        "show",
        parents=[source_parent],
        help="Show the resolved configuration that will be used",
        description=(
            "Print the effective configuration after resolving defaults and paths."
        ),
    )

    config_sub.add_parser(
        "create",
        parents=[source_parent],
        help="Create a default grem.yaml configuration",
        description=(
            "Create a default grem.yaml configuration file.\n\n"
            "The file is created under ~/.config/gremux/default.yaml."
        ),
    )

    # ================================
    # PLACES COMMANDS
    # ================================
    places = sub.add_parser(
        "places",
        help="Manage common project locations",
        description=(
            "Commands for managing places.yaml, which defines common "
            "directories used by the sessionizer."
        ),
    )
    places_sub = places.add_subparsers(
        dest="places_cmd",
        metavar="<subcommand>",
        required=True,
    )

    places_create = places_sub.add_parser(
        "create",
        help="Create or update the places.yaml file",
        description=(
            "Create the places.yaml configuration file, optionally populating "
            "it from an external source such as zoxide."
        ),
    )

    places_create.add_argument(
        "--source",
        "-s",
        metavar="STR",
        help="default, backup, or zoxide",
    )

    places_create.add_argument(
        "--add",
        "-a",
        nargs="+",
        metavar="DIR",
        help="Add one or more directories to places.yaml",
    )

    places_create.add_argument(
        "--maximum",
        "-m",
        type=int,
        metavar="N",
        help="Maximum number of entries to include when using a dynamic source",
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
        # Default behavior: sessionizer
        sessionizer(logger)
