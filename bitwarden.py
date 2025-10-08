"""
bitwarden.py
Bitwarden CSV reader/writer
"""

import csv

from distro import name

BITWARDEN_HEADERS = [
    "folder",
    "favorite",
    "type",
    "name",
    "notes",
    "fields",
    "reprompt",
    "login_uri",
    "login_username",
    "login_password",
    "login_totp",
]


def read(path):
    """Read Bitwarden CSV -> normalized list of dicts."""
    with open(path, newline="", encoding="utf-8-sig") as sf:
        reader = csv.DictReader(sf)
        items = []
        for row in reader:
            item = {
                "name": row.get("name", "").strip(),
                "url": row.get("login_uri", "").strip(),
                "username": row.get("login_username", "").strip(),
                "email": "",  # Bitwarden doesn't separate this — could be in username
                "password": row.get("login_password", "").strip(),
                "note": row.get("notes", "").strip(),
                "totp": row.get("login_totp", "").strip(),
                "vault": row.get("folder", "").strip(),
            }
            items.append(item)
    return items


def write(path, items, force=False):
    """Write normalized items -> Bitwarden CSV."""
    mode = "w" if force else "x"  # 'x' = fail if file exists
    with open(path, mode, newline="", encoding="utf-8") as of:
        writer = csv.DictWriter(of, fieldnames=BITWARDEN_HEADERS)
        writer.writeheader()
        for item in items:
            row = {
                "folder": item.get("vault", ""),
                "favorite": "0",  # default not favorite
                "type": "login",  # assume all are logins
                "name": item.get("name", ""),
                "notes": item.get("note", ""),
                "fields": "",  # advanced fields not mapped
                "login_uri": item.get("url", ""),
                "login_username": item.get("username", ""),
                "login_password": item.get("password", ""),
                "login_totp": item.get("totp", ""),
            }
            writer.writerow(row)
    return len(items)
