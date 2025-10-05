"""
keepass_to_proton.py
Convert a KeePassXC-exported CSV (with the headers you provided) into a Proton Pass CSV:
Proton headers: name,url,email,username,password,note,totp,vault

Usage:
  python keepass_to_proton.py --source keepass_export.csv --out proton_ready.csv
  (defaults: detect utf-8-sig, will not overwrite out unless --force)

Notes:
 - This script assumes your source CSV has headers similar to:
   Group,Title,Username,Password,URL,Notes,TOTP,Icon,Last Modified,Created
 - Email is attempted to be pulled from Username if it looks like an email (contains '@').
 - Inspect the output CSV before importing into Proton Pass. Backup first.
"""
import csv
import argparse
import os
import sys
import re

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

EXPECTED_KEEPASS_HEADERS = [
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


def read_headers(path):
    with detect_encoding_open(path) as fh:
        reader = csv.reader(fh)
        try:
            headers = next(reader)
        except StopIteration:
            headers = []
    return [h.strip() for h in headers]


def find_header(name, headers):
    lname = name.lower()
    for h in headers:
        if h.strip().lower() == lname:
            return h
    return None


def guess_email_from_username(username):
    if not username:
        return ""
    username = username.strip()
    if EMAIL_RE.match(username):
        return username
    return ""


def convert(source_path, out_path, force=False):
    if not os.path.isfile(source_path):
        print("Source file not found:", source_path)
        sys.exit(2)
    if os.path.exists(out_path) and not force:
        print(f"Output file {out_path} already exists. Use --force to overwrite.")
        sys.exit(3)

    source_headers = read_headers(source_path)
    if not source_headers:
        print("No headers detected in source CSV. Is it empty?")
        sys.exit(2)

    mapping = {
        "Group": find_header("Group", source_headers),
        "Title": find_header("Title", source_headers),
        "Username": find_header("Username", source_headers),
        "Password": find_header("Password", source_headers),
        "URL": find_header("URL", source_headers),
        "Notes": find_header("Notes", source_headers),
        "TOTP": find_header("TOTP", source_headers),
    }

    print("\nDetected source headers (first line):")
    print(source_headers)
    print("\nUsing mapping (source header found -> will use):")
    for k, v in mapping.items():
        print(f"  {k:8} -> {v or '(not found)'}")

    if not mapping["Title"] and not mapping["Username"]:
        print(
            "\nWarning: neither Title nor Username found in source headers. Output will miss 'name' and 'username'."
        )
    if not mapping["Password"]:
        print(
            "\nWarning: Password column not found. Output will have empty password fields!"
        )

    with detect_encoding_open(source_path) as sf, open(
        out_path, "w", newline="", encoding="utf-8"
    ) as of:
        reader = csv.DictReader(sf)
        writer = csv.DictWriter(of, fieldnames=PROTON_HEADERS)
        writer.writeheader()

        row_count = 0
        for row in reader:
            row_count += 1
            out = {h: "" for h in PROTON_HEADERS}

            if mapping["Title"]:
                out["name"] = row.get(mapping["Title"], "").strip()
            else:
                out["name"] = (
                    row.get(mapping["Username"], "").strip()
                    if mapping["Username"]
                    else ""
                )

            if mapping["URL"]:
                out["url"] = row.get(mapping["URL"], "").strip()

            if mapping["Username"]:
                out["username"] = row.get(mapping["Username"], "").strip()

            out["email"] = guess_email_from_username(out["username"])

            if mapping["Password"]:
                out["password"] = row.get(mapping["Password"], "").strip()

            if mapping["Notes"]:
                out["note"] = row.get(mapping["Notes"], "").strip()

            if mapping["TOTP"]:
                out["totp"] = row.get(mapping["TOTP"], "").strip()

            if mapping["Group"]:
                out["vault"] = row.get(mapping["Group"], "").strip()

            writer.writerow(out)

    print(f"\nConverted {row_count} rows. Output written to: {out_path}")
    print("Inspect the CSV before importing into Proton Pass.")


def preview_sample(source_path, sample_count=5):
    with detect_encoding_open(source_path) as sf:
        reader = csv.DictReader(sf)
        sample = []
        for i, r in enumerate(reader):
            if i >= sample_count:
                break
            sample.append(r)
    if not sample:
        print("No sample rows to show (source may be empty).")
        return

    print("\n--- SAMPLE SOURCE ROWS (showing relevant fields if present) ---")
    for i, r in enumerate(sample, start=1):
        print(f"\nRow #{i}:")
        for key in EXPECTED_KEEPASS_HEADERS:
            k = next((h for h in r.keys() if h.strip().lower() == key.lower()), None)
            if k:
                val = r.get(k, "")
                if key.lower() in ("password", "totp"):
                    print(f"  {k}: <{len(val)} chars>")
                else:
                    print(f"  {k}: {val}")
    print("\n(Preview masks password/totp content; real conversion will include them.)")


def main():
    ap = argparse.ArgumentParser(
        description="Convert KeePassXC CSV -> Proton Pass CSV (using your provided templates)."
    )
    ap.add_argument("--source", "-s", required=True, help="KeePassXC CSV file (local).")
    ap.add_argument("--out", "-o", help="Output CSV path. Default: <source>_proton.csv")
    ap.add_argument("--force", action="store_true", help="Overwrite output if exists.")
    ap.add_argument(
        "--preview",
        action="store_true",
        help="Show a small preview of source rows (masks sensitive values).",
    )
    args = ap.parse_args()

    source = args.source
    out = args.out or (os.path.splitext(source)[0] + "_proton.csv")

    if args.preview:
        preview_sample(source, sample_count=5)

    convert(source, out, force=args.force)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(130)
