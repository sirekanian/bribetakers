#!/usr/bin/env python3

import json
import os
import re

output = []


def remove_new_lines(x):
    item[x] = re.sub(r' +', ' ', item[x].replace('\n', ' '))


for filename in os.listdir('tmp'):
    for item in json.load(open('tmp/' + filename)):
        if item['0'] and not item['0'].startswith('Name cyrillic'):
            remove_new_lines('0')
            if len(item) == 1:
                print("Skipping empty record: " + item['0'])
                continue
            remove_new_lines('1')
            remove_new_lines('4')
            output += [item]

output.sort(key=lambda x: x['0'].lower())

with open('list-of-war-enablers.json', 'w', encoding='UTF-8') as f:
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
