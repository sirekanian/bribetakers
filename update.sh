#!/usr/bin/env bash

set -e

./update_docs.py
./csv_to_json.py
