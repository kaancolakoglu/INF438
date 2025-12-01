#!/usr/bin/env python3
#mapper3.py
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('"tripduration') or line.startswith('tripduration'):
        continue
    
    try:
        fields = line.split(',')
        start_time = fields[1]  # Format: "YYYY-MM-DD HH:MM:SS"
        hour = start_time.split()[1].split(':')[0]
        print("{}\t1".format(hour))
    except:
        pass
