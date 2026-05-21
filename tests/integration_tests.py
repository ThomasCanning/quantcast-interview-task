# End-to-end tests that invoke the CLI as a real subprocess.
import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLE_LOG = Path(__file__).parent / "cookie_log.csv"
MALFORMED_LOG = Path(__file__).parent / "cookie_log_malformed.csv"
REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "most_active_cookie", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class TestCli:
    # Req 1: basic CLI invocation prints the most active cookie for the given day.
    def test_prints_single_most_active_cookie(self) -> None:
        result = run_cli("-f", str(EXAMPLE_LOG), "-d", "2018-12-09")
        assert result.returncode == 0
        assert result.stdout.splitlines() == ["AtY0laUfhglK3lC7"]

    # Req 7: ties on the target day print every winning cookie, one per line.
    def test_prints_all_tied_cookies_one_per_line(self) -> None:
        result = run_cli("-f", str(EXAMPLE_LOG), "-d", "2018-12-08")
        assert result.returncode == 0
        assert set(result.stdout.splitlines()) == {
            "SAZuXPGUrfbcn5UA",
            "4sMM2LxV07bPJzwf",
            "fbcn5UAVanZf6UtG",
        }

    # Req 8: no cookies on the target day → nothing printed, success exit code.
    def test_prints_nothing_for_missing_day(self) -> None:
        result = run_cli("-f", str(EXAMPLE_LOG), "-d", "2020-01-01")
        assert result.returncode == 0
        assert result.stdout == ""

    # Req 3: missing file → file-not-found error, non-zero exit.
    def test_exits_non_zero_for_missing_file(self, tmp_path: Path) -> None:
        result = run_cli("-f", str(tmp_path / "nope.csv"), "-d", "2018-12-09")
        assert result.returncode == 2
        assert "File not found" in result.stderr

    # Req 4: malformed log → format error, non-zero exit.
    def test_exits_non_zero_for_malformed_log(self) -> None:
        result = run_cli("-f", str(MALFORMED_LOG), "-d", "2018-12-09")
        assert result.returncode == 2
        assert "Could not parse log" in result.stderr

    # Reqs 5 and 6: missing -d or -f → argument error, non-zero exit.
    @pytest.mark.parametrize("missing_flag", [("-d", "2018-12-09"), ("-f", str(EXAMPLE_LOG))])
    def test_rejects_missing_required_arg(self, missing_flag: tuple[str, str]) -> None:
        result = run_cli(*missing_flag)
        assert result.returncode == 2
        assert "the following arguments are required" in result.stderr

    # Req 2: invalid date → argument error, non-zero exit.
    def test_rejects_bad_date_format(self) -> None:
        result = run_cli("-f", str(EXAMPLE_LOG), "-d", "9th-Dec-2018")
        assert result.returncode == 2
        assert "invalid" in result.stderr.lower()
