import argparse

from .display import cmd_country, cmd_company, cmd_trade, cmd_list


def main():
    parser = argparse.ArgumentParser(
        description="Weapons Tracker - Research defense industry data"
    )
    sub = parser.add_subparsers(dest="command")

    p_entity = sub.add_parser(
        "entity", help="Look up a country or regional entity's weapons producers"
    )
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
