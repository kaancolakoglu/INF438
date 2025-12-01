#!/usr/bin/env python3
#mapper2.py
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('"tripduration') or line.startswith('tripduration'):
        continue
    
    try:
        fields = line.split(',')
        usertype = fields[12]
        duration = fields[0]
        print("{}\t{}\t1".format(usertype, duration))
    except:
        pass
