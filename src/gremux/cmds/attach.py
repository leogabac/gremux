import libtmux


def attach(logger) -> None:
    try:
        import questionary
    except ImportError:
        logger.error("questionary is not installed. Install gremux with its dependencies to use `gremux attach`.")
        return None

    try:
        server = libtmux.Server()
    except libtmux.exc.LibTmuxException as exc:
        logger.error(f"tmux is unavailable or returned an error: {exc}")
        return None

    sessions = {session.name: session for session in server.sessions}
    if not sessions:
        logger.info("No active tmux sessions found.")
        return None

    selection = questionary.select(
        "Attach to tmux session:",
        choices=sorted(sessions),
    ).ask()

    if selection is None:
        logger.info("No session selected, exiting...")
        return None

    sessions[selection].attach(exit_=True)

    return None
