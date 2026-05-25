import csv
import sys

from .data import (
    COUNTRIES_DIR,
    COMPANIES_DIR,
    TRADE_FILE,
    load_yaml,
    find_country_file,
    find_company_file,
    guess_country_full_names,
    resolve_country,
)


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
        print(f"Available countries / regional entities ({len(files)}):")
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
