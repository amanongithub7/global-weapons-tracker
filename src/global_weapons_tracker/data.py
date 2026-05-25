from pathlib import Path

import yaml


DATA_DIR = Path(__file__).parent / "data"
COUNTRIES_DIR = DATA_DIR / "countries-and-entities"
COMPANIES_DIR = DATA_DIR / "companies"
TRADE_FILE = DATA_DIR / "trade" / "trade_flows.csv"

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
}


def slugify(name):
    return name.lower().replace(" ", "-")


def find_country_file(query):
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
    slug = slugify(query)
    path = COMPANIES_DIR / f"{slug}.yaml"
    if path.exists():
        return path
    for f in COMPANIES_DIR.glob("*.yaml"):
        if slug in f.stem.lower():
            return f
    return None


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def guess_country_full_names():
    names = {}
    for f in COUNTRIES_DIR.glob("*.yaml"):
        data = load_yaml(f)
        name = data.get("name", "")
        code = data.get("code", "")
        names[name.lower()] = name
        names[code.lower()] = name
    return names


def resolve_country(query, name_map):
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
