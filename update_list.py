#!/usr/bin/env python
"""Updates the list in formats.json. Should be run after any updates to formats, and the result
committed to the repository."""

import argparse
import json
import xml.etree.ElementTree as etree
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("formats_dir", nargs="?", default=Path("formats"), type=Path)
parser.add_argument("-O", "--output-file", default="formats.json")
args = parser.parse_args()

if not args.formats_dir.is_dir():
    print(f"{formats_dir} is not a directory")
    exit(1)

formats = []

for child in args.formats_dir.iterdir():
    if child.suffix != ".xml":
        print(f"skipping {child}")
        continue

    child_root = etree.parse(open(child))
    info = child_root.find("info")

    formats.append({
        "filename": child.name,
        "location": f"https://formats.debatekeeper.czlee.nz/formats/{child.name}",
        "name": child_root.find("name").text,
        "region": info.find("region").text,
        "level": info.find("level").text,
        "used-at": [e.text for e in info.findall("level")],
        "description": info.find("description").text,
    })


with open(args.output_file, "w") as fp:
    json.dump(formats, fp, indent=2)
