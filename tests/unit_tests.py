# Unit tests for parse_log and most_active_cookies.
from datetime import date, datetime, timezone

import pytest

from most_active_cookie.parse_cookies import most_active_cookies, parse_log


def _entry(cookie: str, iso_timestamp: str) -> tuple[str, datetime]:
    return cookie, datetime.fromisoformat(iso_timestamp)


class TestParseLog:
    def test_parses_well_formed_log(self) -> None:
        lines = [
            "cookie,timestamp",
            "abc,2018-12-09T14:19:00+00:00",
            "xyz,2018-12-09T10:13:00+00:00",
        ]
        entries = list(parse_log(lines))

        assert entries == [
            ("abc", datetime(2018, 12, 9, 14, 19, tzinfo=timezone.utc)),
            ("xyz", datetime(2018, 12, 9, 10, 13, tzinfo=timezone.utc)),
        ]

    def test_skips_blank_lines(self) -> None:
        lines = ["cookie,timestamp", "", "abc,2018-12-09T14:19:00+00:00", ""]
        assert [cookie for cookie, _ in parse_log(lines)] == ["abc"]

    # Req 4: incorrect file format is rejected.
    def test_rejects_missing_header(self) -> None:
        with pytest.raises(ValueError, match="Unexpected header"):
            list(parse_log(["abc,2018-12-09T14:19:00+00:00"]))

    # Req 4: incorrect file format is rejected.
    def test_rejects_malformed_row(self) -> None:
        lines = ["cookie,timestamp", "only-one-field"]
        with pytest.raises(ValueError, match="Malformed row on line 2"):
            list(parse_log(lines))

    # Req 4: incorrect file format is rejected.
    def test_rejects_invalid_timestamp(self) -> None:
        lines = ["cookie,timestamp", "abc,not-a-timestamp"]
        with pytest.raises(ValueError):
            list(parse_log(lines))

    # Req 4: incorrect file format is rejected.
    def test_handles_empty_log(self) -> None:
        with pytest.raises(ValueError, match="Unexpected header"):
            list(parse_log([]))


class TestMostActiveCookies:
    # Req 1: returns the most active cookie for the given day.
    def test_returns_single_winner(self) -> None:
        entries = [
            _entry("AtY0laUfhglK3lC7", "2018-12-09T14:19:00+00:00"),
            _entry("SAZuXPGUrfbcn5UA", "2018-12-09T10:13:00+00:00"),
            _entry("5UAVanZf6UtGyKVS", "2018-12-09T07:25:00+00:00"),
            _entry("AtY0laUfhglK3lC7", "2018-12-09T06:19:00+00:00"),
            _entry("SAZuXPGUrfbcn5UA", "2018-12-08T22:03:00+00:00"),
        ]
        assert most_active_cookies(entries, date(2018, 12, 9)) == ["AtY0laUfhglK3lC7"]

    # Req 7: returns every cookie tied for the most active.
    def test_returns_all_ties_in_first_seen_order(self) -> None:
        entries = [
            _entry("SAZuXPGUrfbcn5UA", "2018-12-08T22:03:00+00:00"),
            _entry("4sMM2LxV07bPJzwf", "2018-12-08T21:30:00+00:00"),
            _entry("fbcn5UAVanZf6UtG", "2018-12-08T09:30:00+00:00"),
        ]
        assert most_active_cookies(entries, date(2018, 12, 8)) == [
            "SAZuXPGUrfbcn5UA",
            "4sMM2LxV07bPJzwf",
            "fbcn5UAVanZf6UtG",
        ]

    # Req 8: no cookies on the target day → empty list.
    def test_returns_empty_when_day_absent(self) -> None:
        entries = [_entry("abc", "2018-12-09T14:19:00+00:00")]
        assert most_active_cookies(entries, date(2018, 12, 10)) == []
        assert most_active_cookies(entries, date(2018, 12, 8)) == []

    def test_short_circuits_once_past_target_day(self) -> None:
        consumed: list[str] = []

        def tracking_iter():
            for entry in [
                _entry("a", "2018-12-09T14:00:00+00:00"),
                _entry("b", "2018-12-09T10:00:00+00:00"),
                _entry("c", "2018-12-08T22:00:00+00:00"),
                _entry("should_not_be_seen", "2018-12-07T22:00:00+00:00"),
            ]:
                consumed.append(entry[0])
                yield entry

        result = most_active_cookies(tracking_iter(), date(2018, 12, 9))

        assert result == ["a", "b"]
        assert "should_not_be_seen" not in consumed[:-1]  # break fires on first older row
        assert consumed == ["a", "b", "c"]

    # Covers the planning.md assumption that timezones in the log are normalised
    # to UTC before being bucketed by day.
    def test_normalises_non_utc_timestamps_to_utc(self) -> None:
        # 2018-12-10T01:00:00+05:00 is 2018-12-09T20:00:00 UTC.
        entries = [
            _entry("east", "2018-12-10T01:00:00+05:00"),
            _entry("utc", "2018-12-09T14:00:00+00:00"),
        ]
        assert most_active_cookies(entries, date(2018, 12, 9)) == ["east", "utc"]

    def test_handles_empty_input(self) -> None:
        assert most_active_cookies([], date(2018, 12, 9)) == []
