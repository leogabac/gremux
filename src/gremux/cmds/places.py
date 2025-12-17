import os
import yaml
import subprocess
import math
from gremux.struct.context import PlacesSource


def create(args, logger):
    if args.source is not None:
        create_source(args, logger)
    elif args.add is not None:
        create_add(args, logger)
    else:
        logger.info("Provide any flag --source or --add")


def create_source(args, logger):
    # a bit of validation from enum
    source = PlacesSource(args.source)

    if args.maximum is not None:
        max_items = int(args.maximum)
    else:
        # nothing will ever be greater than this
        max_items = math.inf

    home_dir = os.environ.get("HOME")
    places_file = os.path.join(home_dir, ".config", "gremux", "places.yaml")

    # ===== ZOXIDE SUPPORT ===== #
    if source == PlacesSource.ZOXIDE:
        result = subprocess.run(
            ["zoxide", "query", "--list"],
            capture_output=True,
            text=True,
            check=True,
        )
        result = result.stdout.strip().splitlines()

        if len(result) > max_items:
            result = result[:max_items]

        for path in result:
            logger.info(f"Added {path}")

        places = {"places": result}

    # ===== BACKUP SUPPORT ===== #
    elif source == PlacesSource.BACKUP:
        backup_file = os.path.join(home_dir, ".config", "gremux", "places.bak")
        with open(backup_file) as fh:
            places = yaml.safe_load(fh)

        for path in places["places"]:
            logger.info(f"Added {path}")

    # ===== DEFAULT PLACES ===== #
    elif source == PlacesSource.DEFAULT:
        places = {"places": [home_dir]}

    with open(places_file, "w") as fh:
        yaml.safe_dump(places, fh)

    logger.info(f"Written {places_file}")


def create_add(args, logger):
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

    for path in args.add:
        places["places"].append(path)
        logger.info(f"Added {path} to places.yaml")

    with open(places_file, "w") as fh:
        yaml.safe_dump(places, fh)

    logger.info(f"Written {places_file}")
