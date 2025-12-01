#!/usr/bin/env python3
#reducer3.py

import sys

# Collect all hour counts
hour_counts = {}

for line in sys.stdin:
    key, count = line.strip().split('\t')
    count = int(count)
    
    if key in hour_counts:
        hour_counts[key] += count
    else:
        hour_counts[key] = count

# Output all 24 hours in order
for hour in sorted(hour_counts.keys()):
    print("{}\t{}".format(hour, hour_counts[hour]))

# Output separator and top 5
print("\n--- Top 5 heures les plus actives ---")
top_5 = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:5]
for hour, count in top_5:
    print("{}h: {} trajets".format(hour, count))
