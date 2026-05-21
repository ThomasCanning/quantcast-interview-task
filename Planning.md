Command line program that takes a date and a csv file with lines in the format 'cookie,timestamp' and returns the most frequent cookies for the given day.

## Given assumptions:
- Return multiple cookies on seperate lines if a tie.
- Take in file name with -f and a date with -d
- Log files are sorted by timestamp starting with most recent.
- Timestamps are strings in format YYYY-MM-DDTHH:MM:SS
- Assume enough memory to store contents of the whole file.

## Assumptions I have made that need clarification:

The timestamp on each line is given in YYYY-MM-DDTHH:mm:ss±hh:mm format as a string.

The file and date flags are required arguments.

The timezone of the timestamps in the file are ignored, the day is determined by the date in the flag and timestamps.

# Requirements

1. Can be called from command line by running a command in the form ./ most-active-cookie -f <file-name> -d <date>
e.g. ./ most-active-cookie -f cookie_log.csv -d 2026-05-19

2. If the command is not run with the correct arguments or date, return an argument error.

3. If the file is not found, return a file not found error.

4. If the file is not in the correct format, return a format error.

5. If the date flag is not supplied, return an argument error.

6. If the file flag is not supplied, return an argument error.

7. If multiple cookies are tied for most frequent on the given day, print all of them, one per line.

8. If no cookies are recorded on the given day, print nothing and exit successfully.
