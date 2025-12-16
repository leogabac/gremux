import os
import yaml


def get_places():
    # get the config file
    home_dir = os.environ.get("HOME")
    places_file = os.path.join(home_dir, ".config", "gremux", "places.yaml")

    if not os.path.exists(places_file):
        return None

    with open(places_file) as fh:
        places = yaml.safe_load(fh)

    return places["places"]
