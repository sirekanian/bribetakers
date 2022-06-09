#!/usr/bin/env python3

import json
import os
import requests

os.makedirs('input', exist_ok=True)

html = requests.get('https://acf.international/list-of-war-enablers').text
start_string = """<script id="__NEXT_DATA__" type="application/json">"""
start_index = html.find(start_string) + len(start_string)
end_string = """</script></body></html>"""
end_index = html.find(end_string)
json_document = json.loads(html[start_index:end_index])

with open('input/data.txt', 'w') as f:
    json.dump(json_document, f, indent=2)

docs = []

for group in json_document['props']['pageProps']['villainsListEN']:
    if group['name'] == 'Full sanctions list':
        for doc in group['lists']:
            if doc['name'].startswith('Contributors to the war'):
                docs += [doc]

if len(docs) != 3:
    raise Exception('Wrong number of docs: ' + str(len(docs)))

with open('input/data1.txt', 'w') as f:
    json.dump(docs, f, indent=2)

for doc in docs:
    _, ext = os.path.splitext(doc['file'])
    print('Downloading data' + ext)
    with open('input/data' + ext, 'wb') as f:
        f.write(requests.get(doc['file']).content)
