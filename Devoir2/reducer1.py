#!/usr/bin/env python3
#reducer1.py

import sys

# Collect all station counts
station_counts = {}

for line in sys.stdin:
    key, count = line.strip().split('\t')
    count = int(count)
    
    if key in station_counts:
        station_counts[key] += count
    else:
        station_counts[key] = count

# Sort by count descending and get top 10
top_10 = sorted(station_counts.items(), key=lambda x: x[1], reverse=True)[:10]

# Output top 10
for station, count in top_10:
    print("{}\t{}".format(station, count))
