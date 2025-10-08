"""
keepass.py
KeePassXC CSV reader
"""

import csv
import re

EXPECTED_HEADERS = [
    "Group",
    "Title",
    "Username",
    "Password",
    "URL",
    "Notes",
    "TOTP",
    "Icon",
    "Last Modified",
    "Created",
]

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def detect_encoding_open(path):
    return open(path, newline="", encoding="utf-8-sig")


def read(path):
    """Read KeePass CSV -> normalized list of dicts."""
    with detect_encoding_open(path) as sf:
        reader = csv.DictReader(sf)
        items = []
        for row in reader:
            username = row.get("Username", "").strip()
            item = {
                "name": row.get("Title", "").strip() or username,
                "url": row.get("URL", "").strip(),
                "username": username,
                "email": username if EMAIL_RE.match(username) else "",
                "password": row.get("Password", "").strip(),
                "note": row.get("Notes", "").strip(),
                "totp": row.get("TOTP", "").strip(),
                "vault": row.get("Group", "").strip(),
            }
            items.append(item)
    return items
