#!/usr/bin/env bash
cp -f token_map.yaml "token_map.$(date +%Y%m%d-%H%M%S).yaml.bak"
python3 validator.py --project-name valuator --input token_map.yaml --outdir out
