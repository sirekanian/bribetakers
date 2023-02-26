#!/usr/bin/env python3

import csv
import json
import os
import re

output = []

with open('input/data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for k in row:
            if k not in {'Description', 'Tags'}:
                row[k] = row[k].replace('\n', ' ')
            row[k] = re.sub(r' +', ' ', row[k].strip())
        if len(row) != 8:
            raise Exception('Wrong length of row: ' + str(row))
        tags = []
        for t in row['Tags'].split('\n'):
            tag = t.strip()
            if tag:
                tags += [tag]
        output += [{
            '0': row['Name ru'],
            '1': row['Name en'],
            '2': row['DOB'],
            '3': row['Gender'],
            '4': row['Description'],
            '5': tags,
        }]

output.sort(key=lambda x: x['0'].lower())

with open('list-of-war-enablers.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

with open("README.md", "r") as f:
    lines = f.readlines()

with open("README.md", "w") as f:
    for line in lines:
        f.write(re.sub(r'/count-\d+-red', f'/count-{len(output)}-red', line))

actual = len(output)
expected = None

for doc in json.load(open('input/data1.txt')):
    _, ext = os.path.splitext(doc['file'])
    if ext == '.csv':
        expected = doc['number']

result = '[OK]' if actual == expected else '[FAIL]'
print(result + ' Actual: ' + str(actual) + ', expected: ' + str(expected))
