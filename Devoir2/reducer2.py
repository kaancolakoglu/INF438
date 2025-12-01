#!/usr/bin/env python3
#reducer2.py

import sys

current_key = None
total_duration = 0
count = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    key = parts[0]
    duration = int(parts[1])
    
    if current_key == key:
        total_duration += duration
        count += 1
    else:
        if current_key:
            avg = total_duration / count if count > 0 else 0
            print("{}\t{}\t{:.2f}".format(current_key, count, avg))
        current_key = key
        total_duration = duration
        count = 1

if current_key:
    avg = total_duration / count if count > 0 else 0
    print("{}\t{}\t{:.2f}".format(current_key, count, avg))
