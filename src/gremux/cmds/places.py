import os
import yaml
from gremux.struct.context import PlacesSource


def create(args, logger):
    if args.source is not None:
        create_source(args.source, logger)
    elif args.add is not None:
        create_add(args.add, logger)
    else:
        logger.info("Provide any flag --source or --add")


def create_source(source, logger):
    # a bit of validation from enum
    source = PlacesSource(source)

    home_dir = os.environ.get("HOME")
    places_file = os.path.join(home_dir, ".config", "gremux", "places.yaml")

    if source == PlacesSource.ZOXIDE:
        logger.info("Not implemented! Exiting.")
        return
    elif source == PlacesSource.DEFAULT:
        places = {"places": [home_dir]}

    with open(places_file, "w") as fh:
        yaml.safe_dump(places, fh)

    logger.info(f"Written {places_file}")


def create_add(paths, logger):
    home_dir = os.environ.get("HOME")
    places_file = os.path.join(home_dir, ".config", "gremux", "places.yaml")

    if not os.path.exists(places_file):
        message = [
            "places.yml is not configred! Run.",
            "gremux places create -s SOURCE",
            "Exiting",
        ]
        logger.info("\n".join(message))
        return

    with open(places_file) as fh:
        places = yaml.safe_load(fh)

    for path in paths:
        places["places"].append(path)
        logger.info(f"Added {path} to places.yaml")

    with open(places_file, "w") as fh:
        yaml.safe_dump(places, fh)

    logger.info(f"Written {places_file}")
