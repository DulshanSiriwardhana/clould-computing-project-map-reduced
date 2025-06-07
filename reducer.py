#!/usr/bin/env python3
import sys

current_popularity = None
total_followers = 0.0
count = 0

for line in sys.stdin:
    try:
        popularity, followers = line.strip().split('\t')
        popularity = int(popularity)
        followers = float(followers)  # <- correct here

        if current_popularity == popularity:
            total_followers += followers
            count += 1
        else:
            if current_popularity is not None:
                avg = total_followers / count
                print(f"{current_popularity}\t{avg:.2f}")
            current_popularity = popularity
            total_followers = followers
            count = 1
    except:
        continue

if current_popularity is not None and count > 0:
    avg = total_followers / count
    print(f"{current_popularity}\t{avg:.2f}")
