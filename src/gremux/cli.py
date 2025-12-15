from gremux.parser import Parser


def main():
    import argparse

    parser = argparse.ArgumentParser("gremux")
    sub = parser.add_subparsers(dest="cmd", required=True)


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
        parser = Parser()
        grem = parser.grem()
        print(grem)

    elif args.cmd == "down":

        raise NotImplementedError("Work in progress!")
        print("down")
    elif args.cmd == "attach":

        raise NotImplementedError("Work in progress!")
        print("attach")
