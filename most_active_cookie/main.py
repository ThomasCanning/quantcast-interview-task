# Entry Point
import argparse
import sys
from datetime import date

from .parse_cookies import most_active_cookies, parse_log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print the most active cookie(s) for a given date.",
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the cookie CSV file.")
    parser.add_argument(
        "-d", "--date", required=True, type=date.fromisoformat, dest="target_date",
        help="Target date in YYYY-MM-DD format.",
    )
    args = parser.parse_args(argv)
    
    try:
        with open(args.file) as log_file:
            cookies = most_active_cookies(parse_log(log_file), args.target_date)
    except FileNotFoundError:
        print(f"File not found: {args.file}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Could not parse log: {exc}", file=sys.stderr)
        return 2

    for cookie in cookies:
        print(cookie)
    return 0
