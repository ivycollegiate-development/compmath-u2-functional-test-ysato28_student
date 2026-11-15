"""Task 1 — load and clean threats_raw.csv with an audit trail.

Starter file. The plumbing is done for you; the judgements are not.
Fill in the four functions marked TODO. You may add an import if you want one
(`io` is allowed); the rest does not need to change.

Read the packet (§4.1) next to this file. The order of the nine steps is part
of the task — several of them break if you reorder them.

Run it with:

    python3 clean_threats.py

A finished run prints a per-drop audit and ends with "All checks passed".
"""

import csv

# ---------------------------------------------------------------------------
# Fixed configuration — already correct, do not change
# ---------------------------------------------------------------------------

RAW_PATH = "threats_raw.csv"
CLEAN_PATH = "threats_clean.csv"

# Written out by hand on purpose. Do not rebuild this from a dict: dict key
# order is insertion order, and a cleaner that emits the wrong column order
# still writes a file that opens fine.
HEADER = ["date", "phishing_reports", "failed_logins", "login_success_rate"]

# One dict, not scattered if-statements. A bound is a claim about what is
# physically possible in the world, not about what is typical.
BOUNDS = {
    "phishing_reports": (0, 1000),
    "failed_logins": (0, 10000),
    "login_success_rate": (0.0, 1.0),
}

# Count columns are whole numbers -> int. The rate is a fraction -> float.
CONVERT = {
    "phishing_reports": int,
    "failed_logins": int,
    "login_success_rate": float,
}

REASONS = ("blank", "unparseable", "impossible")


# ---------------------------------------------------------------------------
# TODO 1 — steps 1 and 2: open the file, then strip the comment lines
# ---------------------------------------------------------------------------
def read_data_lines(path):
    """Return the file's lines with blank lines and '#' comments removed.

    Open it with open(path, newline="") — packet step 1. The newline argument is
    the documented way to hand a file to the csv module.

    Must strip whitespace before testing, so an indented "  # comment" is
    still treated as a comment.
    """
    raise NotImplementedError("TODO 1: implement read_data_lines() — packet §4.1 steps 1-2")


# ---------------------------------------------------------------------------
# TODO 2 — steps 3 and 4: parse with DictReader and confirm the header
# ---------------------------------------------------------------------------
def parse_rows(lines):
    """Parse the surviving lines with csv.DictReader and validate the header.

    Return a list of row dicts. Raise ValueError (with the actual header in
    the message) if the header is not exactly HEADER, in that order.

    DictReader accepts any iterable of lines, so the list from TODO 1 works
    directly — no temporary file needed. (io.StringIO is also allowed.)
    """
    raise NotImplementedError("TODO 2: implement parse_rows() — packet §4.1 steps 3-4")


# ---------------------------------------------------------------------------
# TODO 3 — steps 6 and 7: clean one row, in a fixed order (step 5 is BOUNDS above)
# ---------------------------------------------------------------------------
def clean_row(row, drops):
    """Return the row with numeric values, or None if it must be dropped.

    Fixed order for every column: blank -> unparseable -> impossible.
    - blank: drop, reason "blank <column>"
    - unparseable: drop, reason "unparseable <column>"
    - impossible: drop, reason "impossible <column>=<value-as-written>"
    On a pass, replace the string with its numeric value.

    Print each drop as it happens:
        Dropped row: blank <column>
    and increment `drops` once per dropped row, keyed by the category word alone
    ('blank', 'unparseable', 'impossible') — not the full reason string.

    `drops` is {"blank": 0, "unparseable": 0, "impossible": 0}. Mutate it; do
    not reassign it.

    Return the same dict, modified, with `date` unchanged. Falling off the end
    of the function returns None, and main() treats None as a drop.
    """
    raise NotImplementedError("TODO 3: implement clean_row() — packet §4.1 steps 6-7")


# ---------------------------------------------------------------------------
# TODO 4 — step 9 (write half): emit threats_clean.csv
# ---------------------------------------------------------------------------
def write_clean(path, rows):
    """Write HEADER then one line per row, using csv.writer and this order.

    Open the output with newline="" as well, or csv's line endings double up.
    """
    raise NotImplementedError("TODO 4: implement write_clean() — packet §4.1 step 9")


# ---------------------------------------------------------------------------
# Plumbing — already correct, do not change
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

    assert set(drops) == set(REASONS), (
        "Unknown drop category in {} — key `drops` by the category word only".format(
            sorted(drops)
        )
    )

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
