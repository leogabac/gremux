import os
import yaml
import subprocess
import math
from pathlib import Path
from gremux.struct.context import PlacesSource


def _config_dir() -> Path:
    return Path.home() / ".config" / "gremux"


def create(args, logger) -> None:
    if args.source is not None:
        create_source(args, logger)
    elif args.add is not None:
        create_add(args, logger)
    else:
        logger.info("Provide any flag --source or --add")

    return None


def create_source(args, logger) -> None:
    # a bit of validation from enum
    source = PlacesSource(args.source)

    if args.maximum is not None:
        max_items = int(args.maximum)
    else:
        # nothing will ever be greater than this
        max_items = math.inf

    home_dir = str(Path.home())
    config_dir = _config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    places_file = config_dir / "places.yaml"

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
        backup_file = config_dir / "places.bak"
        with backup_file.open() as fh:
            places = yaml.safe_load(fh)

        for path in places["places"]:
            logger.info(f"Added {path}")

    # ===== DEFAULT PLACES ===== #
    elif source == PlacesSource.DEFAULT:
        places = {"places": [home_dir]}

    with places_file.open("w") as fh:
        yaml.safe_dump(places, fh)

    logger.info(f"Written {places_file}")

    return None


def create_add(args, logger) -> None:
    places_file = _config_dir() / "places.yaml"

    if not places_file.exists():
        message = [
            "places.yml is not configred! Run.",
            "gremux places create -s SOURCE",
            "Exiting",
        ]
        logger.info("\n".join(message))
        return None

    with places_file.open() as fh:
        places = yaml.safe_load(fh)

    for path in args.add:
        places["places"].append(path)
        logger.info(f"Added {path} to places.yaml")

    with places_file.open("w") as fh:
        yaml.safe_dump(places, fh)

    logger.info(f"Written {places_file}")

    return None
