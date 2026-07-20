import logging
from pathlib import Path
import gremux.struct as gst
import libtmux
import os
import shlex
import subprocess
import yaml


def _config_dir() -> Path:
    return Path.home() / ".config" / "gremux"


def _templates_dir() -> Path:
    return _config_dir() / "templates"


def _template_names() -> list[str]:
    templates_dir = _templates_dir()
    if not templates_dir.exists():
        return []

    return sorted(path.stem for path in templates_dir.glob("*.yaml") if path.is_file())


def _load_yaml_file(path: Path) -> dict | None:
    with path.open() as fh:
        return yaml.safe_load(fh)


def _write_yaml_file(path: Path, data: dict) -> None:
    with path.open("w") as fh:
        yaml.safe_dump(data, fh, sort_keys=False)


def _set_session_name(data: dict | None, name: str) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Config file must contain a top-level mapping")

    session = data.get("session")
    if not isinstance(session, dict):
        raise ValueError("Config file must define a top-level 'session' mapping")

    session["name"] = name
    return data


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
                        "name": "main",
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
    elif args.source == "session":
        _create_from_current_session(args, logger)
    else:
        logger.info("Feature not available. Exiting.")

    return None


def _project_root() -> Path:
    """Return the current Git root, falling back to the working directory."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return Path.cwd()

    return Path(result.stdout.strip())


def _current_tmux_session(server: libtmux.Server):
    pane_id = os.environ.get("TMUX_PANE")
    if pane_id is None:
        raise ValueError("Run this command from inside the tmux session to export.")

    result = server.cmd("display-message", "-p", "-t", pane_id, "#{session_id}")
    if not result.stdout:
        raise ValueError("Could not determine the current tmux session.")

    sessions = server.sessions.filter(session_id=result.stdout[0])
    if not sessions:
        raise ValueError("The current tmux session is no longer available.")

    return sessions[0]


def _pane_cwd(pane, project_root: Path) -> str:
    pane_path = Path(pane.pane_current_path)
    try:
        relative_path = pane_path.relative_to(project_root)
    except ValueError:
        return str(pane_path)

    return "." if relative_path == Path(".") else str(relative_path)


def _infer_layout(panes) -> str | None:
    """Choose a portable named layout from the current pane geometry."""
    if len(panes) <= 1:
        return None

    lefts = [int(pane.pane_left) for pane in panes]
    tops = [int(pane.pane_top) for pane in panes]
    widths = [int(pane.pane_width) for pane in panes]
    heights = [int(pane.pane_height) for pane in panes]

    if len(set(lefts)) == 1:
        return "even-vertical"
    if len(set(tops)) == 1:
        return "even-horizontal"

    widest = max(widths)
    tallest = max(heights)
    if any(width == widest and height == tallest for width, height in zip(widths, heights)):
        return "main-vertical" if widest > tallest else "main-horizontal"

    # Gremux supports named tmux layouts rather than opaque geometry strings.
    # Keep every exported pane by choosing a deterministic tiled-like fallback.
    return "even-vertical"


def _session_config(session, project_root: Path) -> dict:
    windows = []
    for window in session.windows:
        window_panes = list(window.panes)
        panes = [
            {
                "cwd": _pane_cwd(pane, project_root),
                "command": None,
            }
            for pane in window_panes
        ]
        windows.append(
            {
                "name": window.name,
                "layout": _infer_layout(window_panes),
                "panes": panes,
            }
        )

    return {"session": {"name": session.name, "windows": windows}}


def _create_from_current_session(args, logger) -> None:
    project_root = _project_root()
    target_file = project_root / "grem.yaml"

    if target_file.exists() and not args.force:
        logger.error(
            f"Refusing to overwrite existing file: {target_file}. "
            "Use --force to replace it."
        )
        return None

    try:
        session = _current_tmux_session(libtmux.Server())
        data = _session_config(session, project_root)
        _write_yaml_file(target_file, data)
    except (libtmux.exc.LibTmuxException, OSError, ValueError) as exc:
        logger.error(f"Failed to export the current tmux session: {exc}")
        return None

    logger.info(f"Exported current tmux session to {target_file}")
    return None


def use(args, logger) -> None:
    template_name = args.name

    if args.interactive:
        try:
            import questionary
        except ImportError:
            logger.error("questionary is not installed. Install gremux with its dependencies to use `config use --interactive`.")
            return None

        templates = _template_names()
        if not templates:
            logger.info(f"No templates found in {_templates_dir()}")
            return None

        template_name = questionary.select(
            "Choose a template:",
            choices=templates,
        ).ask()

        if template_name is None:
            logger.info("No template selected, exiting...")
            return None

    if template_name is None:
        logger.error("Must provide NAME or use --interactive.")
        return None

    template_file = _templates_dir() / f"{template_name}.yaml"
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

    try:
        data = _load_yaml_file(template_file)
        data = _set_session_name(data, Path.cwd().name)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        logger.error(f"Failed to prepare template config: {exc}")
        return None

    _write_yaml_file(target_file, data)
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

    try:
        data = _load_yaml_file(source_file)
        data = _set_session_name(data, args.name)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        logger.error(f"Failed to prepare local config: {exc}")
        return None

    _write_yaml_file(target_file, data)
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
