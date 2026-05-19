Command line program that takes a date and a csv file with lines in the format 'cookie,timestamp' and returns the most frequent cookies for the given day.

To install, test, and run:

```bash
make install        # installs into a local .venv
make test           # runs the unit and integration tests
make run            # runs against an example file
make global-install # installs it on PATH globally via pipx (requires pipx)
```

```bash
most-active-cookie -f <path-to-log.csv> -d <YYYY-MM-DD>
```

- `-f` / `--file`: path to the cookie log CSV.
- `-d` / `--date`: target date in UTC (`YYYY-MM-DD`).


Testing:

Unit tests cover the parser and counting function directly, including ties, missing days, timezone normalisation, malformed input, and the short-circuit behaviour on sorted input.

Integration tests run the cli and call it with test cases that catch argument parsing errors and expect error codes.
