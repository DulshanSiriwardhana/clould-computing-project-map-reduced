#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin)
try:
    header = next(reader)  # Skip header
except StopIteration:
    sys.exit(0)  # empty input

for row in reader:
    print("DEBUG row:", row, file=sys.stderr)  # print to stderr so it doesn't interfere with mapper output
    try:
        if len(row) < 5:
            continue

        followers_raw = row[1].strip()
        popularity_raw = row[4].strip()

        if followers_raw.lower() == "null" or popularity_raw.lower() == "null":
            continue
        if not followers_raw or not popularity_raw:
            continue

        followers = float(followers_raw)
        popularity = int(float(popularity_raw))

        print(f"{popularity}\t{followers}")

    except (ValueError, IndexError) as e:
        print(f"DEBUG error: {e}", file=sys.stderr)
        continue
