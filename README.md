# Unit 2 Functional Test — Campus Network Threat Data

## Test Overview

50-minute live coding test on the VPS. Closed notes, no browser, no AI.

1. **Load & Clean** `threats_raw.csv` with an audit trail (`clean_threats.py`) — 20 pts
2. **Chart 1**: Daily timeline of phishing reports + failed logins (`project_charts.py`) — 10 pts
3. **Chart 2**: Weekday vs weekend average phishing reports (same file) — 10 pts
4. **Analysis**: Three-paragraph `analysis.md` (audience, key number, limitation each) — 10 pts

## Setup

Your own repo already exists and already contains the data. **Do not run `git init`.**

```bash
cd ~
git clone https://github.com/ivycollegiate-development/compmath-u2-functional-test-$(whoami)_student.git functional-test
cd functional-test
ls
```

You should see `threats_raw.csv` in this directory. **Do not modify the raw CSV.**

## Files in this repo

- `threats_raw.csv` — the raw dataset (8 comment lines, 61 data rows, intentional defects)
- `README.md` — this file

## Submission

Write your scripts in this directory, then commit and push:

```bash
git add .
git commit -m "Unit 2 functional test submission"
git push origin main
git log --oneline -1
```

Paste the `git log --oneline -1` line (commit hash + message) into the Classroom
assignment **U2 Functional Test — Live Coding**.

No PR is needed — you push straight to your own repo.

**Password prompt = Personal Access Token, not your GitHub password.**

If the push fails, keep working locally and tell me at the end — I will collect the
work from the VPS directly.
