''' Extracts counties by state from EPA file '''

import csv
from operator import itemgetter
from collections import defaultdict

# Open CSV file
f = open('daily_44201_2021.csv')
rows = csv.reader(f)
next(rows)                      # Ignore header line

result = defaultdict(set)       # Store counties only once
for fields in rows:
    state = fields[24]
    county = fields[25]
    result[state].add(county)   # County not duplicated in a set

# Sort by state
result = sorted(result.items(), key = itemgetter(0))
for state, counties in result:
    print(state)
    for county in sorted(counties):     # Sort counties
        print('\t', county, sep='')
