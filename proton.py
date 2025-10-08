"""
proton.py
Proton Pass CSV writer
"""

import csv

PROTON_HEADERS = [
    "name",
    "url",
    "email",
    "username",
    "password",
    "note",
    "totp",
    "vault",
]


def write(path, items, force=False):
    """Write normalized items -> Proton Pass CSV."""
    mode = "w" if force else "x"  # 'x' = fail if file exists
    with open(path, mode, newline="", encoding="utf-8") as of:
        writer = csv.DictWriter(of, fieldnames=PROTON_HEADERS)
        writer.writeheader()
        for item in items:
            row = {h: item.get(h, "") for h in PROTON_HEADERS}
            writer.writerow(row)
    return len(items)
