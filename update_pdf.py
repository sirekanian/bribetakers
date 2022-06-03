#!/usr/bin/env python3

import json
import requests

html = requests.get('https://acf.international/list-of-war-enablers').text
start_string = """<script id="__NEXT_DATA__" type="application/json">"""
start_index = html.find(start_string) + len(start_string)
end_string = """</script></body></html>"""
end_index = html.find(end_string)
json_document = json.loads(html[start_index:end_index])

with open('bribetakers.txt', 'w') as f:
    json.dump(json_document, f, indent=2)

items = []

for group in json_document['props']['pageProps']['villainsListEN']:
    if group['name'] == 'Full sanctions list':
        for item in group['lists']:
            if item['name'] == 'Contributors to the war, pdf':
                items += [item]

if len(items) != 1:
    raise Exception('Wrong number of items')

with open('bribetakers1.txt', 'w') as f:
    json.dump(items[0], f, indent=2)

with open('bribetakers.pdf', 'wb') as f:
    f.write(requests.get(items[0]['file']).content)
