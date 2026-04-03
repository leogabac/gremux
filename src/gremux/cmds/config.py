import logging
from pathlib import Path
import gremux.struct as gst
import libtmux
import os
import shlex
import shutil
import subprocess
import yaml


def _config_dir() -> Path:
    return Path.home() / ".config" / "gremux"


def _templates_dir() -> Path:
    return _config_dir() / "templates"


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


def use(args, logger) -> None:
    template_file = _templates_dir() / f"{args.name}.yaml"
    target_file = Path.cwd() / "grem.yaml"

    if not template_file.exists():
        logger.error(f"Template not found: {template_file}")
        return None

    if target_file.exists() and not args.force:
        logger.error(
            f"Refusing to overwrite existing file: {target_file}. "
            "Use --force to replace it."
        )
        return None

    shutil.copyfile(template_file, target_file)
    logger.info(f"Copied {template_file} to {target_file}")

    return None


def list_templates(args, logger) -> None:
    templates_dir = _templates_dir()

    if not templates_dir.exists():
        logger.info(f"No templates directory found: {templates_dir}")
        return None

    templates = sorted(path.stem for path in templates_dir.glob("*.yaml") if path.is_file())

    if not templates:
        logger.info(f"No templates found in {templates_dir}")
        return None

    for name in templates:
        print(name)

    return None


def save(args, logger) -> None:
    source_file = Path.cwd() / "grem.yaml"
    templates_dir = _templates_dir()
    target_file = templates_dir / f"{args.name}.yaml"

    if not source_file.exists():
        logger.error(f"Local config not found: {source_file}")
        return None

    templates_dir.mkdir(parents=True, exist_ok=True)

    if target_file.exists() and not args.force:
        logger.error(
            f"Refusing to overwrite existing template: {target_file}. "
            "Use --force to replace it."
        )
        return None

    shutil.copyfile(source_file, target_file)
    logger.info(f"Copied {source_file} to {target_file}")

    return None


def edit(args, logger) -> None:
    editor = os.environ.get("EDITOR")
    if not editor:
        logger.error("EDITOR is not set. Set $EDITOR to launch your preferred editor.")
        return None

    config_dir = _config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)

    cmd = shlex.split(editor) + [str(config_dir)]

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        logger.error(f"Editor binary not found: {cmd[0]}")
    except subprocess.CalledProcessError as exc:
        logger.error(f"Editor exited with code {exc.returncode}.")

    return None
