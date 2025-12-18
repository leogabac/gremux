import os
import yaml
from typing import List
import subprocess


def get_places() -> List:
    """
    Load the places.yaml file and return the list of common places in the system.
    """

    home_dir = os.environ.get("HOME")
    places_file = os.path.join(home_dir, ".config", "gremux", "places.yaml")

    if not os.path.exists(places_file):
        return None

    with open(places_file) as fh:
        places = yaml.safe_load(fh)

    return places["places"]


def fzf_select(logger, dirs):
    """Prompt user to select a directory using fzf."""
    if not dirs:
        return None

    try:
        # Pass the list of dirs to fzf via stdin
        result = subprocess.run(
            ["fzf", "--prompt=Select directory: "],
            input="\n".join(dirs),
            text=True,
            capture_output=True,
            check=True,
        )
        selection = result.stdout.strip()
        return selection if selection else None

    except FileNotFoundError:
        # fallback if fzf binary is not installed
        logger.error("fzf binary not found. Please install fzf.")
        return None
