import logging
from gremux.cmds import sessionizer
from gremux.cmds.attach import attach
import gremux.cmds.places as plc
import gremux.cmds.config as cfg
import gremux.struct as struct


VERSION = "0.1.2-dev"


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
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
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

    config_use = config_sub.add_parser(
        "use",
        help="Copy a saved template into the current project",
        description=(
            "Copy ~/.config/gremux/templates/<name>.yaml into the current "
            "directory as grem.yaml."
        ),
    )
    config_use.add_argument(
        "name",
        metavar="NAME",
        help="Template name to copy from ~/.config/gremux/templates/",
    )
    config_use.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing local grem.yaml",
    )

    config_list = config_sub.add_parser(
        "list",
        help="List saved templates",
        description="List template names under ~/.config/gremux/templates/.",
    )

    config_save = config_sub.add_parser(
        "save",
        help="Save the current project's grem.yaml as a template",
        description=(
            "Copy the current directory's grem.yaml into "
            "~/.config/gremux/templates/<name>.yaml."
        ),
    )
    config_save.add_argument(
        "name",
        metavar="NAME",
        help="Template name to write under ~/.config/gremux/templates/",
    )
    config_save.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing saved template",
    )

    config_sub.add_parser(
        "edit",
        help="Open the gremux config directory in your editor",
        description="Open ~/.config/gremux/ in the editor defined by $EDITOR.",
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

    attach_cmd = sub.add_parser(
        "attach",
        help="Interactively attach to an existing tmux session",
        description=(
            "Show active tmux sessions and attach to the one you select."
        ),
    )
    attach_cmd.add_argument(
        "--last",
        "-l",
        action="store_true",
        help="Use tmux's default attach behavior instead of showing a picker",
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
        elif args.config_cmd == "list":
            cfg.list_templates(args, logger)
        elif args.config_cmd == "save":
            cfg.save(args, logger)
        elif args.config_cmd == "edit":
            cfg.edit(args, logger)
        elif args.config_cmd == "use":
            cfg.use(args, logger)

    elif args.cmd == "places":
        if args.places_cmd == "create":
            plc.create(args, logger)

    elif args.cmd == "attach":
        attach(args, logger)

    else:
        # Default behavior: sessionizer
        sessionizer(logger)
