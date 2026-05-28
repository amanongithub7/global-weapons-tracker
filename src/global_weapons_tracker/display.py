"""CLI display (print) functions.

Each ``cmd_*`` function corresponds to a CLI subcommand. They
consume data via :mod:`~global_weapons_tracker.api` and format it for
terminal output.  No data-querying or file-resolution logic lives here.
"""

import sys

from . import api


def cmd_trade(args):
    """Query and display weapons trade flows filtered by origin / destination."""
    result = api.get_trade_flows(from_=args.from_country, to_=args.to_country)
    flows = result["flows"]

    if not flows:
        print("No trade flows found matching your query.")
        return

    total = result["total_value"]
    source = result["source"]
    print(f"\n{'TRADE FLOWS':^60}")
    print(f"{'=' * 60}")
    print(f"  {'From':16s} -> {'To':16s} | {'Value (USD)':>14s} | Category")
    print(f"  {'-' * 56}")
    for r in flows:
        val = int(r["estimated_value_usd"])
        cat = r.get("category", "")
        print(
            f"  {r['from_country']:16s} -> {r['to_country']:16s} | ${val:>12,} | {cat}"
        )
    print(f"  {'-' * 56}")
    print(f"  {'Total':16s}   {'':16s} | ${total:>12,}")
    print(f"\nSource: {source}")


def cmd_list(args):
    """List available entities, companies, or trade flows."""
    if args.list_type == "entities":
        entities = api.get_entity_list()
        print(f"Available countries / regional entities ({len(entities)}):")
        for e in entities:
            print(f"  {e['name']:25s} ({e['code']})")
    elif args.list_type == "companies":
        companies = api.get_company_list()
        print(f"Available companies ({len(companies)}):")
        for c in companies:
            print(f"  {c['name']}")
    elif args.list_type == "trade":
        print("Trade flows (see `trade` command for filtered queries)")


def cmd_country(args):
    """Display entity / country details: producers, exports, imports, sources."""
    data = api.get_entity(args.query)
    if not data:
        print(f"Country not found: {args.query}")
        sys.exit(1)

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
    """Display company details: programs, subsidiaries, suppliers, sources."""
    data = api.get_company(args.query)
    if not data:
        print(f"Company not found: {args.query}")
        sys.exit(1)

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
