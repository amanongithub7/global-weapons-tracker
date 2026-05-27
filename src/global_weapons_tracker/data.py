"""Data-loading layer for the Global Weapons Tracker.

Provides paths to the bundled YAML / CSV data, a slug map for fuzzy
country/entity lookups, and helper functions for resolving queries to
files on disk.
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


def find_country_file(query):
    """Locate a country/entity YAML file by name or alias.

    Attempts an exact slug lookup first via ``REGION_NAME_TO_SLUG``,
    then falls back to a fuzzy substring match against all filenames
    in the countries directory.

    Parameters
    ----------
    query : str
        Country name, code, or partial alias (e.g. ``"usa"``, ``"us"``,
        ``"United States"``).

    Returns
    -------
    Path or None
        Resolved path to the YAML file, or ``None`` if no match found.
    """
    key = query.lower().strip()
    slug = REGION_NAME_TO_SLUG.get(key, key)
    path = COUNTRIES_DIR / f"{slug}.yaml"
    if path.exists():
        return path
    for f in COUNTRIES_DIR.glob("*.yaml"):
        if slug in f.stem.lower():
            return f
    return None


def find_company_file(query):
    """Locate a company YAML file by name.

    Attempts an exact slug match first, then falls back to a fuzzy
    substring match against all filenames in the companies directory.

    Parameters
    ----------
    query : str
        Company name (e.g. ``"Lockheed Martin"``, ``"Rostec"``).

    Returns
    -------
    Path or None
        Resolved path to the YAML file, or ``None`` if no match found.
    """
    slug = slugify(query)
    path = COMPANIES_DIR / f"{slug}.yaml"
    if path.exists():
        return path
    for f in COMPANIES_DIR.glob("*.yaml"):
        if slug in f.stem.lower():
            return f
    return None


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


def guess_country_full_names():
    """Build a lookup dictionary of lowercase aliases to official names.

    Reads every YAML file in ``COUNTRIES_DIR`` and maps both the
    ``name`` and ``code`` fields (lowercased) to the official name.

    Returns
    -------
    dict[str, str]
        Mapping of lowercase aliases to full country names.
    """
    names = {}
    for f in COUNTRIES_DIR.glob("*.yaml"):
        data = load_yaml(f)
        name = data.get("name", "")
        code = data.get("code", "")
        names[name.lower()] = name
        names[code.lower()] = name
    return names


def resolve_country(query, name_map):
    """Resolve a free-form query to the canonical country name.

    Checks the provided ``name_map`` first, then falls back to
    ``REGION_NAME_TO_SLUG``, and finally attempts a substring match.

    Parameters
    ----------
    query : str or None
        User-provided country query (e.g. ``"India"``, ``"IN"``).
    name_map : dict[str, str]
        Mapping produced by :func:`guess_country_full_names`.

    Returns
    -------
    str or None
        Canonical country name if resolved, or the original query
        unchanged if no resolution was possible.
    """
    if not query:
        return None
    q = query.lower().strip()
    if q in name_map:
        return name_map[q]
    if q in REGION_NAME_TO_SLUG:
        slug = REGION_NAME_TO_SLUG[q]
        path = COUNTRIES_DIR / f"{slug}.yaml"
        if path.exists():
            d = load_yaml(path)
            return d.get("name")
    for alias, full in name_map.items():
        if q in alias:
            return full
    return query
