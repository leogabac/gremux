import os
import yaml
from typing import List
import subprocess
from pathlib import Path


def get_places() -> List:
    """
    Load the places.yaml file and return the list of common places in the system.
    """

    places_file = Path.home() / ".config" / "gremux" / "places.yaml"

    if not places_file.exists():
        return None

    with places_file.open() as fh:
        places = yaml.safe_load(fh)

    if not isinstance(places, dict):
        raise ValueError("places.yaml must contain a top-level mapping")

    result = places.get("places")
    if not isinstance(result, list):
        raise ValueError("places.yaml must define a list under 'places'")

    return result


def fzf_select(logger, dirs):
    """Prompt user to select a directory using fzf."""
    if not dirs:
        return None

    try:
        result = subprocess.run(
            ["fzf", "--prompt=Select directory: "],
            input="\n".join(dirs),
            text=True,
            capture_output=True,
            check=True,
        )
        selection = result.stdout.strip()
        return selection if selection else None

    except KeyboardInterrupt:
        # User pressed Ctrl-C
        logger.debug("fzf selection cancelled by user")
        return None

    except subprocess.CalledProcessError as e:
        # fzf exits with:
        # 130 -> Ctrl-C
        # 1   -> Esc / no selection
        if e.returncode in (1, 130):
            logger.debug("fzf exited without selection")
            return None
        logger.error(f"fzf failed with exit code {e.returncode}.")
        return None

    except FileNotFoundError:
        logger.error("fzf binary not found. Please install fzf.")
        return None
