#!/usr/bin/env python3
"""Print TEI <table> elements and counts for parsed benchmark papers."""

from __future__ import annotations

import sys
from pathlib import Path
from xml.etree import ElementTree as ET


TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    parsed_dir = base_dir / "parsed"

    if not parsed_dir.exists():
        print(f"Parsed directory not found: {parsed_dir}", file=sys.stderr)
        return 1

    xml_files = sorted(parsed_dir.glob("*.xml"))
    if not xml_files:
        print(f"No TEI XML files found in {parsed_dir}", file=sys.stderr)
        return 1

    for xml_file in xml_files:
        print(f"=== {xml_file.name} ===")
        try:
            root = ET.parse(xml_file).getroot()
        except ET.ParseError as exc:
            print(f"PARSE_ERROR: {exc}")
            continue

        tables = root.findall(".//tei:table", TEI_NS)
        print(f"table_count: {len(tables)}")
        if not tables:
            print("(no tables found)")
            continue

        for idx, table in enumerate(tables, start=1):
            print(f"--- table {idx} ---")
            table_text = ET.tostring(table, encoding="unicode")
            print(table_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
