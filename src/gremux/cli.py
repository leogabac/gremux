from gremux.cmds import sessionizer


def main():
    import argparse

    parser = argparse.ArgumentParser("gremux")
    sub = parser.add_subparsers(dest="cmd", required=False)

    # if nothign is provided, make the default to open something like
    # tmuxify to let the user choose something from a set of common locations
    # this common set might be useful to set up the first time and save on the config file?

    sub.add_parser("up")
    # create a tmux session based on local config file

    sub.add_parser("show")
    # show the config file

    sub.add_parser("load")
    # on my current session, apply the config file

    sub.add_parser("create")
    # from a session, create a config file

    sub.add_parser("archive")
    # find the archive at ~/.confg/gremux

    # gremux archive save
    # save as "template" some config file from a project

    # gremux archive set
    # set to cur project from something saved on the archive

    args = parser.parse_args()

    if args.cmd == "up":
        raise NotImplementedError("Work in progress!")

    elif args.cmd == "show":
        raise NotImplementedError("Work in progress!")

    elif args.cmd == "load":
        raise NotImplementedError("Work in progress!")

    elif args.cmd == "create":
        raise NotImplementedError("Work in progress!")

    elif args.cmd == "archive":
        raise NotImplementedError("Work in progress!")
    else:
        sessionizer()
