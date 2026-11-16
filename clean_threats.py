"""Task 1 — load and clean threats_raw.csv with an audit trail.

WORKED SOLUTION. Every function is filled in: run it and it ends with
"All checks passed". The comments carry the reasoning, because Task 4 asks you
to justify each decision — copy the code, but read why it is shaped this way.

Run it with:

    python3 clean_threats.py

It writes threats_clean.csv. It never modifies threats_raw.csv.
"""

import csv

# ---------------------------------------------------------------------------
# Fixed configuration
# ---------------------------------------------------------------------------

RAW_PATH = "threats_raw.csv"
CLEAN_PATH = "threats_clean.csv"

# Written out by hand on purpose. Do not rebuild this from a dict: dict key
# order is insertion order, and a cleaner that emits the wrong column order
# still writes a file that opens fine — so the mistake survives inspection.
HEADER = ["date", "phishing_reports", "failed_logins", "login_success_rate"]

# One dict, not scattered if-statements. A bound is a claim about what is
# physically possible in the world, not about what is typical: 0 reports and
# 1000 reports are both possible, so both stay; -3 reports, or a success rate
# of 1.4 in a column stored as a fraction, cannot be true, so those rows go.
BOUNDS = {
    "phishing_reports": (0, 1000),
    "failed_logins": (0, 10000),
    "login_success_rate": (0.0, 1.0),
}

# Count columns are whole numbers -> int. The rate is a fraction -> float.
# csv.DictReader hands you strings, always, so this conversion is not optional:
# a chart built on r["failed_logins"] without it plots categories, not numbers,
# and matplotlib will not warn you.
CONVERT = {
    "phishing_reports": int,
    "failed_logins": int,
    "login_success_rate": float,
}

REASONS = ("blank", "unparseable", "impossible")


# ---------------------------------------------------------------------------
# Steps 1 and 2 — open the file, then strip the comment lines
# ---------------------------------------------------------------------------
def read_data_lines(path):
    """Return the file's lines with blank lines and '#' comments removed.

    open(path, newline="") is the documented way to hand a file to the csv
    module. The comment stripping must happen *before* DictReader sees the
    data: DictReader reads the first line it is given as the header, so a file
    that opens with comments gives every column the wrong name and raises
    nothing at all. That is the "quietly wrong" bug this task is built around.
    """
    with open(path, newline="") as handle:
        text = handle.read()

    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:                # blank line
            continue
        if stripped.startswith("#"):    # stripping first catches "  # ..."
            continue
        lines.append(line)
    return lines


# ---------------------------------------------------------------------------
# Steps 3 and 4 — parse with DictReader and confirm the header
# ---------------------------------------------------------------------------
def parse_rows(lines):
    """Parse the surviving lines with csv.DictReader and validate the header.

    DictReader accepts any iterable of lines, so the list from step 2 works
    directly — no temporary file and no io.StringIO needed. Checking the header
    here means a missing or misordered column fails at the top with a readable
    message, instead of four lines later as a bare KeyError.
    """
    reader = csv.DictReader(lines)
    if reader.fieldnames != HEADER:
        raise ValueError(
            "Unexpected header {!r} — expected {!r}".format(
                reader.fieldnames, HEADER
            )
        )
    return list(reader)


# ---------------------------------------------------------------------------
# Steps 6 and 7 — clean one row, in a fixed order (step 5 is BOUNDS above)
# ---------------------------------------------------------------------------
def clean_row(row, drops):
    """Return the row with numeric values, or None if it must be dropped.

    Fixed order for every column: blank -> unparseable -> impossible.

    The order is not cosmetic. A blank cell tested after conversion is a
    ValueError from int("") — a crash instead of a drop. A bounds test placed
    before conversion compares a string to a number — a TypeError. And getting
    the *category* right is worth more than the row count: a row rejected for
    the wrong reason is a bug in your code, not bad data.

    One hole worth knowing: float("nan") passes both bounds comparisons
    (neither < nor > is true), so a nan cell would survive as "clean". This
    file has none. A stricter cleaner would test math.isnan first.

    In this file exactly two rows drop: one blank phishing_reports, and one
    login_success_rate of 1.4.
    """
    for column in HEADER[1:]:
        raw = row[column]

        # blank — nothing, or whitespace, in the cell
        if raw is None or str(raw).strip() == "":
            print("Dropped row: blank {}".format(column))
            drops["blank"] += 1
            return None

        # unparseable — something that is not a number at all
        try:
            value = CONVERT[column](str(raw).strip())
        except ValueError:
            print("Dropped row: unparseable {}".format(column))
            drops["unparseable"] += 1
            return None

        # impossible — it is a number, and the number cannot be true
        low, high = BOUNDS[column]
        if value < low or value > high:
            print("Dropped row: impossible {}={}".format(column, raw))
            drops["impossible"] += 1
            return None

        row[column] = value

    # The same dict, modified, with date untouched. Falling off the end would
    # return None and main() would treat the row as a drop — so this line is
    # load-bearing, not decoration.
    return row


# ---------------------------------------------------------------------------
# Step 9, write half — emit threats_clean.csv
# ---------------------------------------------------------------------------
def write_clean(path, rows):
    """Write HEADER then one line per row, using csv.writer and this order.

    newline="" on the output as well, or csv's \r\n doubles up to \r\r\n.
    The header is written from HEADER, never from the dict's keys.
    """
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        for row in rows:
            writer.writerow([row[column] for column in HEADER])


# ---------------------------------------------------------------------------
# Steps 8 and 9, audit half
# ---------------------------------------------------------------------------
def main():
    lines = read_data_lines(RAW_PATH)
    rows = parse_rows(lines)

    rows_in = len(rows)
    drops = {reason: 0 for reason in REASONS}
    kept = []

    for row in rows:
        cleaned = clean_row(dict(row), drops)
        if cleaned is None:
            continue
        kept.append(cleaned)

    rows_out = len(kept)
    rows_dropped = rows_in - rows_out

    # Step 8. A genuine assertion, not a comment: if the counts disagree the
    # script must die, because a wrong cleanup that reports success is worse
    # than one that fails loudly.
    assert rows_in == rows_out + sum(drops.values()), (
        "Count mismatch: rows_in={} rows_out={} drops={}".format(
            rows_in, rows_out, drops
        )
    )

    write_clean(CLEAN_PATH, kept)

    print("Rows in: {}".format(rows_in))
    print("Rows out: {}".format(rows_out))
    print("Rows dropped: {}  {}".format(rows_dropped, drops))
    print("All checks passed")


if __name__ == "__main__":
    main()
