"""Tasks 2 and 3 — chart the cleaned threat log.

WORKED SOLUTION for both charts. Run clean_threats.py first: this script reads
its output (threats_clean.csv), never the raw file. Everything below is
commented with the reason it is written that way, because Task 4 asks you to
point at the exact line that makes each chart honest.

Run it with:

    python3 clean_threats.py
    python3 project_charts.py

Produces chart1_timeline.png and chart2_weekday_weekend.png.
"""

import csv
from datetime import datetime

import matplotlib
matplotlib.use("Agg")          # the PNG is the deliverable, not a window
import matplotlib.pyplot as plt

CLEAN_PATH = "threats_clean.csv"


# ---------------------------------------------------------------------------
# Load once, for both charts
# ---------------------------------------------------------------------------
def load_clean_rows(path):
    """Read threats_clean.csv back in and convert at load, not at plot time.

    plt.plot accepts a list of numeric *strings* without raising and draws a
    meaningless categorical axis, so the int() calls happen here, in the list
    comprehension, where you can see them:

        phishing = [int(r["phishing_reports"]) for r in rows]

    Chart 2 filters these same lists — it never re-reads the CSV and never
    re-converts a cell, so both charts are guaranteed to describe one dataset.
    """
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))

    dates = [row["date"] for row in rows]
    phishing = [int(row["phishing_reports"]) for row in rows]
    failed = [int(row["failed_logins"]) for row in rows]
    return rows, dates, phishing, failed


def is_weekend(date_text):
    """True for Saturday and Sunday.

    Parse the real date: weekday() is 0 for Monday through 6 for Sunday, so
    >= 5 is the weekend. Comparing the string against "Sat"/"Sun" cannot work —
    this file stores full ISO dates.
    """
    return datetime.strptime(date_text, "%Y-%m-%d").weekday() >= 5


# ---------------------------------------------------------------------------
# Task 2 — Chart 1: daily timeline
# ---------------------------------------------------------------------------
def chart1_timeline(dates, phishing, failed):
    """Two series on one pair of axes, titled with a finding."""

    plt.figure(figsize=(10, 5))

    plt.plot(dates, phishing, marker="o", label="Phishing reports")
    plt.plot(dates, failed, marker="s", label="Failed logins")

    plt.xlabel("Date")
    plt.ylabel("Count")            # both series are counts — say so
    plt.ylim(bottom=0)             # Unit 2 principle 1: never a floating axis
    plt.legend()

    # The title is a finding, not a subject. The peak date is computed from the
    # data on this run, so it cannot drift from the plot. "Move Together" and
    # "Both Peak" are words, not calculations — the assert below is what makes
    # them true of this file rather than merely plausible.
    peak_count = max(phishing)
    peak_index = phishing.index(peak_count)
    peak_date = dates[peak_index]
    assert dates[failed.index(max(failed))] == peak_date, (
        "the two series do not peak on the same day — retitle the chart"
    )
    plt.title(
        "Phishing and Failed Logins Move Together; Both Peak on {}".format(peak_date)
    )

    # One label per day is a grey smear at ~60 dates. Every point stays
    # plotted; only every fourth tick gets a label, plus the peak day, so the
    # date named in the title can actually be found on the axis.
    ticks = sorted(set(range(0, len(dates), 4)) | {peak_index})
    plt.xticks(ticks, [dates[i] for i in ticks], rotation=45, ha="right")

    # AFTER the labels exist. tight_layout computes the margins from the
    # rotated tick labels that are already on the axis; call it first and the
    # saved margins are measured for labels that are not there yet.
    plt.tight_layout()

    # savefig before anything that clears or closes the figure. On an
    # interactive backend, closing the show() window destroys the figure and a
    # later savefig writes a blank PNG — invisible unless you open the file.
    # Under Agg (set above) show() is a no-op, so it is never called here.
    plt.savefig("chart1_timeline.png", dpi=150, bbox_inches="tight")
    plt.clf()                      # Chart 2 is drawn next in this same script


# ---------------------------------------------------------------------------
# Task 3 — Chart 2: weekday vs weekend
# ---------------------------------------------------------------------------
def chart2_weekday_weekend(dates, phishing):
    """Two bars: the average phishing reports per day type."""

    # Filter the lists Chart 1 already loaded and converted. Zipping date to
    # value keeps the pairing honest without touching the CSV again.
    weekday_vals = [v for d, v in zip(dates, phishing) if not is_weekend(d)]
    weekend_vals = [v for d, v in zip(dates, phishing) if is_weekend(d)]

    # Guard both groups: sum(...) / len(...) on an empty group raises
    # ZeroDivisionError, and Chart 1 is already saved by the time we get here.
    if not weekday_vals or not weekend_vals:
        print("one day-type group is empty — Chart 2 skipped")
        return

    # Divide by the rows each group actually contains — never by 7, never by a
    # hardcoded day count. sum(weekend) / 14 is wrong and does not crash.
    avg_wd = sum(weekday_vals) / len(weekday_vals)
    avg_we = sum(weekend_vals) / len(weekend_vals)

    print(
        "weekday {:.2f} ({} days) | weekend {:.2f} ({} days)".format(
            avg_wd, len(weekday_vals), avg_we, len(weekend_vals)
        )
    )

    plt.figure(figsize=(6, 4))
    bars = plt.bar(["Weekday", "Weekend"], [avg_wd, avg_we])

    # Label above each bar, not through it.
    for bar, value in zip(bars, [avg_wd, avg_we]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            "{:.2f}".format(value),
            ha="center",
            va="bottom",
        )

    plt.ylabel("Average phishing reports")
    # Headroom is not a truncated axis: the bottom stays at zero, the top gets
    # 18% of air so the bar label is not cut in half by the plot boundary.
    plt.ylim(0, max(avg_wd, avg_we) * 1.18)
    plt.title(
        "Weekdays Average {:.2f} Phishing Reports vs Weekends {:.2f}".format(
            avg_wd, avg_we
        )
    )
    plt.tight_layout()

    plt.savefig("chart2_weekday_weekend.png", dpi=150, bbox_inches="tight")
    plt.clf()


def main():
    # `rows` is not used by these two charts; it is returned so later charts
    # (the login-success-rate histogram, in the project repo) can filter rows.
    rows, dates, phishing, failed = load_clean_rows(CLEAN_PATH)
    chart1_timeline(dates, phishing, failed)
    chart2_weekday_weekend(dates, phishing)


if __name__ == "__main__":
    main()
