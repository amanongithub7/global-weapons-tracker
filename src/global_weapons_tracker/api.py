"""Programmatic API for querying weapons tracker data.

Pure data-access functions that return Python objects (dicts/lists).
Consumers (CLI display, frontend, scripts) can format the returned
data however they want.
"""

import csv
from pathlib import Path
from typing import Any

from .data import (
    COMPANIES_DIR,
    COUNTRIES_DIR,
    REGION_NAME_TO_SLUG,
    TRADE_FILE,
    load_yaml,
    slugify,
)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _find_country_file(query: str) -> Path | None:
    key = query.lower().strip()
    slug = REGION_NAME_TO_SLUG.get(key, key)
    path = COUNTRIES_DIR / f"{slug}.yaml"
    if path.exists():
        return path
    for f in COUNTRIES_DIR.glob("*.yaml"):
        if slug in f.stem.lower():
            return f
    return None


def _find_company_file(query: str) -> Path | None:
    slug = slugify(query)
    path = COMPANIES_DIR / f"{slug}.yaml"
    if path.exists():
        return path
    for f in COMPANIES_DIR.glob("*.yaml"):
        if slug in f.stem.lower():
            return f
    return None


def _guess_country_full_names() -> dict[str, str]:
    names = {}
    for f in COUNTRIES_DIR.glob("*.yaml"):
        data = load_yaml(f)
        name = data.get("name", "")
        code = data.get("code", "")
        names[name.lower()] = name
        names[code.lower()] = name
    return names


def _resolve_country(query: str | None, name_map: dict[str, str]) -> str | None:
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


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_entity(query: str) -> dict | None:
    """Look up a country/entity by name or alias and return its full data dict.

    Parameters
    ----------
    query : str
        Country name, code, or alias (e.g. ``"India"``, ``"IN"``, ``"us"``).

    Returns
    -------
    dict or None
        Parsed YAML content as a nested dict, or ``None`` if not found.
    """
    path = _find_country_file(query)
    if not path:
        return None
    return load_yaml(path)


def get_entity_list() -> list[dict[str, Any]]:
    """Return a summary dict for every country/entity on file.

    Returns
    -------
    list[dict]
        Each entry contains ``name``, ``code``, ``region``, and ``slug`` keys.
    """
    result = []
    for f in sorted(COUNTRIES_DIR.glob("*.yaml")):
        data = load_yaml(f)
        result.append(
            {
                "name": data.get("name", ""),
                "code": data.get("code", ""),
                "region": data.get("region", ""),
                "slug": f.stem,
            }
        )
    return result


def get_company(query: str) -> dict | None:
    """Look up a company by name and return its full data dict.

    Parameters
    ----------
    query : str
        Company name (e.g. ``"Lockheed Martin"``, ``"DICON"``).

    Returns
    -------
    dict or None
        Parsed YAML content as a nested dict, or ``None`` if not found.
    """
    path = _find_company_file(query)
    if not path:
        return None
    return load_yaml(path)


def get_company_list() -> list[dict[str, Any]]:
    """Return a summary dict for every company on file.

    Returns
    -------
    list[dict]
        Each entry contains ``name``, ``type``, ``country``, and ``slug`` keys.
    """
    result = []
    for f in sorted(COMPANIES_DIR.glob("*.yaml")):
        data = load_yaml(f)
        result.append(
            {
                "name": data.get("name", ""),
                "type": data.get("type", ""),
                "country": data.get("country", ""),
                "slug": f.stem,
            }
        )
    return result


def get_trade_flows(
    from_: str | None = None,
    to_: str | None = None,
) -> dict[str, Any]:
    """Query trade flows with optional origin / destination filters.

    Parameters
    ----------
    from_ : str or None
        Filter by origin country name/code. ``None`` means no filter.
    to_ : str or None
        Filter by destination country name/code. ``None`` means no filter.

    Returns
    -------
    dict
        ``flows`` — list of matching row dicts (keys match CSV columns).\n
        ``total_value`` — sum of ``estimated_value_usd`` across matched rows.\n
        ``source`` — the source attribution string from the first matched row.
    """
    if not TRADE_FILE.exists():
        return {"flows": [], "total_value": 0, "source": ""}

    name_map = _guess_country_full_names()
    from_q = _resolve_country(from_, name_map)
    to_q = _resolve_country(to_, name_map)

    with open(TRADE_FILE, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    matched = []
    source = ""
    for row in rows:
        from_match = (
            not from_q
            or from_q.lower() == row["from_country"].lower()
            or from_q.lower() == row["from_code"].lower()
        )
        to_match = (
            not to_q
            or to_q.lower() == row["to_country"].lower()
            or to_q.lower() == row["to_code"].lower()
        )
        if from_match and to_match:
            matched.append(dict(row))
            if not source:
                source = row.get("source", "SIPRI Arms Transfers Database")

    total = sum(int(r["estimated_value_usd"]) for r in matched)

    return {
        "flows": matched,
        "total_value": total,
        "source": source,
    }
