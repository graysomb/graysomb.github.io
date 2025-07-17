#!/usr/bin/env python3
"""
Script to generate a JSON manifest of ad image filenames.

Run this script after adding/removing files in images/ads/ to update js/ads.json.
"""
import os
import json

# Determine directories
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ads_dir = os.path.join(base_dir, 'images', 'ads')
js_dir = os.path.join(base_dir, 'js')

# List ad files (ignore hidden files)
files = [f for f in os.listdir(ads_dir) if not f.startswith('.')]

# Build manifest
manifest = {'ads': files}

# Write manifest to js/ads.json
out_path = os.path.join(js_dir, 'ads.json')
with open(out_path, 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"Generated ads manifest with {len(files)} entries at {out_path}")