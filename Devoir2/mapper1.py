#!/usr/bin/env python3
#mapper1.py
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('"tripduration') or line.startswith('tripduration'):
        continue
    
    try:
        fields = line.split(',')
        start_station_name = fields[4]
        print("{}\t1".format(start_station_name))
    except:
        pass
