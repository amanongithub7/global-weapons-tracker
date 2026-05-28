"""Low-level data I/O for the Global Weapons Tracker.

Provides file-system paths to bundled data, a slug map for
country/entity alias resolution, and YAML-loading helpers.
Query resolution lives in :mod:`api`; this module only handles
constants and file I/O.
"""

from pathlib import Path

import yaml


DATA_DIR = Path(__file__).parent / "data"
"""Path: Root directory for all bundled data files."""

COUNTRIES_DIR = DATA_DIR / "countries-and-entities"
"""Path: Directory containing per-country YAML files."""

COMPANIES_DIR = DATA_DIR / "companies"
"""Path: Directory containing per-company YAML files."""

TRADE_FILE = DATA_DIR / "trade" / "trade_flows.csv"
"""Path: CSV file containing bilateral trade-flow records."""

REGION_NAME_TO_SLUG = {
    "united states": "usa",
    "us": "usa",
    "usa": "usa",
    "russia": "russia",
    "ru": "russia",
    "china": "china",
    "cn": "china",
    "germany": "germany",
    "de": "germany",
    "india": "india",
    "in": "india",
    "turkey": "turkey",
    "tr": "turkey",
    "israel": "israel",
    "il": "israel",
    "france": "france",
    "fr": "france",
    "united kingdom": "uk",
    "uk": "uk",
    "gb": "uk",
    "italy": "italy",
    "it": "italy",
    "spain": "spain",
    "es": "spain",
    "south korea": "south-korea",
    "kr": "south-korea",
    "south africa": "south-africa",
    "za": "south-africa",
    "uae": "uae",
    "united arab emirates": "uae",
    "taiwan": "taiwan",
    "tw": "taiwan",
    "pakistan": "pakistan",
    "pk": "pakistan",
    "singapore": "singapore",
    "sg": "singapore",
    "indonesia": "indonesia",
    "id": "indonesia",
    "philippines": "philippines",
    "ph": "philippines",
    "mexico": "mexico",
    "mx": "mexico",
    "canada": "canada",
    "ca": "canada",
    "argentina": "argentina",
    "ar": "argentina",
    "brazil": "brazil",
    "br": "brazil",
    "ethiopia": "ethiopia",
    "et": "ethiopia",
    "democratic republic of the congo": "dr-congo",
    "dr congo": "dr-congo",
    "congo dr": "dr-congo",
    "congo": "dr-congo",
    "cd": "dr-congo",
    "sudan": "sudan",
    "sd": "sudan",
    "south sudan": "south-sudan",
    "ss": "south-sudan",
    "mali": "mali",
    "ml": "mali",
    "nigeria": "nigeria",
    "ng": "nigeria",
}
"""dict[str, str]: Mapping of country names / codes to YAML filename slugs."""


def slugify(name):
    """Convert a human-readable name into a filename-friendly slug.

    Parameters
    ----------
    name : str
        Arbitrary string (e.g. ``"Lockheed Martin"``).

    Returns
    -------
    str
        Lowercased string with spaces replaced by hyphens.
    """
    return name.lower().replace(" ", "-")


def load_yaml(path):
    """Load and parse a YAML file.

    Parameters
    ----------
    path : Path
        Path to a ``.yaml`` file on disk.

    Returns
    -------
    dict
        Parsed YAML content as a Python dictionary.
    """
    with open(path) as f:
        return yaml.safe_load(f)


