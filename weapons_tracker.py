import argparse
import csv
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Required: PyYAML. Install with: pip install pyyaml")
    sys.exit(1)


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
    "south korea": "south-korea",
    "kr": "south-korea",
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
    """Build a dict mapping lowercase aliases -> full country names for trade matching."""
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


def cmd_trade(args):
    if not TRADE_FILE.exists():
        print(f"Trade data not found at {TRADE_FILE}")
        sys.exit(1)

    name_map = guess_country_full_names()
    from_q = resolve_country(args.from_country, name_map)
    to_q = resolve_country(args.to_country, name_map)

    with open(TRADE_FILE) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    matched = []
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
            matched.append(row)

    if not matched:
        print("No trade flows found matching your query.")
        return

    total = sum(int(r["estimated_value_usd"]) for r in matched)
    print(f"\n{'TRADE FLOWS':^60}")
    print(f"{'=' * 60}")
    print(f"  {'From':16s} -> {'To':16s} | {'Value (USD)':>14s} | Category")
    print(f"  {'-' * 56}")
    for r in matched:
        val = int(r["estimated_value_usd"])
        cat = r.get("category", "")
        print(
            f"  {r['from_country']:16s} -> {r['to_country']:16s} | ${val:>12,} | {cat}"
        )
    print(f"  {'-' * 56}")
    print(f"  {'Total':16s}   {'':16s} | ${total:>12,}")

    print(f"\nSource: {matched[0].get('source', 'SIPRI')}" if matched else "")


def cmd_list(args):
    if args.list_type == "entities":
        files = sorted(COUNTRIES_DIR.glob("*.yaml"))
        print(f"Available countries ({len(files)}):")
        for f in files:
            data = load_yaml(f)
            code = data.get("code", "")
            print(f"  {data['name']:25s} ({code})")
    elif args.list_type == "companies":
        files = sorted(COMPANIES_DIR.glob("*.yaml"))
        print(f"Available companies ({len(files)}):")
        for f in files:
            data = load_yaml(f)
            print(f"  {data['name']}")
    elif args.list_type == "trade":
        print("Trade flows (see `trade` command for filtered queries)")


def cmd_country(args):
    path = find_country_file(args.query)
    if not path:
        print(f"Country not found: {args.query}")
        print("Try: python weapons_tracker.py list countries")
        sys.exit(1)
    data = load_yaml(path)

    print(f"\n{'=' * 60}")
    print(f"  {data['name']} ({data['code']}) - {data.get('region', '')}")
    print(f"{'=' * 60}\n")

    print(f"{'PRODUCERS':^60}")
    print(f"{'-' * 60}")
    for p in data.get("producers", []):
        print(f"\n  {p['name']}")
        print(f"  {'Type:':<12} {p.get('type', 'N/A')}")
        rev = p.get("revenue")
        rv = p.get("revenue_year")
        if rev:
            print(f"  {'Revenue:':<12} ${rev} ({rv})")
        emp = p.get("employees")
        if emp:
            if isinstance(emp, int):
                print(f"  {'Employees:':<12} {emp:,}")
            else:
                print(f"  {'Employees:':<12} {emp}")
        prods = p.get("products", [])
        if prods:
            print(f"  {'Products:':<12}")
            for prod in prods:
                print(f"    - {prod}")
        notes = p.get("notes")
        if notes:
            print(f"  {'Notes:':<12} {notes}")

    exports = data.get("top_export_destinations", [])
    if exports:
        print(f"\n{'TOP EXPORT DESTINATIONS':^60}")
        print(f"{'-' * 60}")
        for e in exports:
            n = e.get("notes", "")
            print(f"  {e['country']:20s} {n}")

    imports_ = data.get("top_import_sources", [])
    if imports_:
        print(f"\n{'TOP IMPORT SOURCES':^60}")
        print(f"{'-' * 60}")
        for i in imports_:
            n = i.get("notes", "")
            print(f"  {i['country']:20s} {n}")

    print(f"\n{'SOURCES':^60}")
    print(f"{'-' * 60}")
    for s in data.get("sources", []):
        print(f"  - {s['name']}")
        print(f"    {s['url']}")


def cmd_company(args):
    path = find_company_file(args.query)
    if not path:
        print(f"Company not found: {args.query}")
        print("Try: python weapons_tracker.py list companies")
        sys.exit(1)
    data = load_yaml(path)

    print(f"\n{'=' * 60}")
    print(f"  {data['name']}")
    print(f"{'=' * 60}")
    print(f"  Country:  {data.get('country', 'N/A')}")
    print(f"  Type:     {data.get('type', 'N/A')}")
    print(f"  Founded:  {data.get('founded', 'N/A')}")

    programs = data.get("key_programs", [])
    if programs:
        print(f"\n{'KEY PROGRAMS':^60}")
        print(f"{'-' * 60}")
        for prog in programs:
            print(f"\n  {prog['name']}")
            print(f"    Type:   {prog.get('type', 'N/A')}")
            print(f"    Status: {prog.get('status', 'N/A')}")
            desc = prog.get("description", "")
            if desc:
                print(f"    Desc:   {desc}")
            uc = prog.get("unit_cost")
            if uc:
                print(f"    Cost:   ${uc}")
            ec = prog.get("export_clients", [])
            if ec:
                print(f"    Export: {', '.join(ec)}")

    subsidiaries = data.get("subsidiaries", [])
    if subsidiaries:
        print(f"\n{'SUBSIDIARIES':^60}")
        print(f"{'-' * 60}")
        for sub in subsidiaries:
            prods = sub.get("products", [])
            print(f"  {sub['name']}")
            if prods:
                print(f"    Products: {', '.join(prods)}")

    suppliers = data.get("suppliers", [])
    if suppliers:
        print(f"\n{'SUPPLIERS':^60}")
        print(f"{'-' * 60}")
        for s in suppliers:
            print(f"\n  {s['name']}")
            print(f"    Country:    {s.get('country', 'N/A')}")
            print(f"    Supplies:   {s.get('supplies', 'N/A')}")
            print(f"    Relation:   {s.get('relationship', 'N/A')}")

    print(f"\n{'SOURCES':^60}")
    print(f"{'-' * 60}")
    for s in data.get("sources", []):
        print(f"  - {s['name']}")
        print(f"    {s['url']}")


def main():
    parser = argparse.ArgumentParser(
        description="Weapons Tracker - Research defense industry data"
    )
    sub = parser.add_subparsers(dest="command")

    p_entity = sub.add_parser("entity", help="Look up a country or regional entity's weapons producers")
    p_entity.add_argument(
        "query",
        help="Entity name or code (e.g., 'usa', 'russia', 'india')",
    )

    p_company = sub.add_parser(
        "company", help="Look up a company's details and supply chain"
    )
    p_company.add_argument(
        "query", help="Company name (e.g., 'Lockheed Martin', 'Rostec')"
    )

    p_trade = sub.add_parser("trade", help="Query weapons trade flows")
    p_trade.add_argument("--from", dest="from_country", help="Filter by origin country")
    p_trade.add_argument(
        "--to", dest="to_country", help="Filter by destination country"
    )

    p_list = sub.add_parser("list", help="List available data")
    p_list.add_argument(
        "list_type", choices=["entities", "companies", "trade"], help="What to list"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cmds = {
        "entity": cmd_country,
        "company": cmd_company,
        "trade": cmd_trade,
        "list": cmd_list,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
