import csv
from collections import Counter
from datetime import date, datetime, timezone


# Parse the log into (cookie, timestamp) pairs.
def parse_log(lines: list[str]) -> list[tuple[str, datetime]]:
    reader = csv.reader(lines)
    header = next(reader, None)
    if header != ["cookie", "timestamp"]:
        raise ValueError(f"Unexpected header: {header!r}, expected ['cookie', 'timestamp']")

    entries = []
    for line_number, row in enumerate(reader, start=2):
        if not row:
            continue
        if len(row) != 2:
            raise ValueError(f"Malformed row on line {line_number}: {row!r}")
        cookie, timestamp_str = row
        entries.append((cookie, datetime.fromisoformat(timestamp_str)))
    return entries


# Return the cookie(s) seen most often on the target date.
def most_active_cookies(entries: list[tuple[str, datetime]], target_date: date) -> list[str]:
    counts: Counter[str] = Counter()
    # Iterate through cookie-date pairs
    # For pairs where the date is the entry date, iterate counter for that cookie
    # Stop when passed target date as entries are ordered
    for cookie, timestamp in entries:
        entry_date = timestamp.astimezone(timezone.utc).date()
        if entry_date > target_date:
            continue
        if entry_date < target_date:
            break
        counts[cookie] += 1

    if not counts:
        return []

    top_count = max(counts.values())
    cookies_to_return = []
    for cookie, count in counts.items():
        if count == top_count:
            cookies_to_return.append(cookie)
    return cookies_to_return
