"""
main.py
Generic password manager converter
"""

import argparse
import importlib
import os
import sys


def main():
    ap = argparse.ArgumentParser(description="Password manager CSV converter")
    ap.add_argument("--source", "-s", required=True, help="Source CSV file.")
    ap.add_argument("--out", "-o", help="Output CSV file. Default: <source>_<to>.csv")
    ap.add_argument(
        "--from",
        "-f",
        required=True,
        dest="from_fmt",
        help="Source password manager (e.g., keepass)",
    )
    ap.add_argument(
        "--to",
        "-t",
        required=True,
        dest="to_fmt",
        help="Target password manager (e.g., proton)",
    )
    ap.add_argument("--force", action="store_true", help="Overwrite output if exists.")
    args = ap.parse_args()

    # dynamic import based on flag
    try:
        src_mod = importlib.import_module(args.from_fmt)
        dst_mod = importlib.import_module(args.to_fmt)
    except ModuleNotFoundError as e:
        print(f"Converter module not found: {e}")
        sys.exit(2)

    out = args.out or (os.path.splitext(args.source)[0] + f"_{args.to_fmt}.csv")

    # read → write
    items = src_mod.read(args.source)
    try:
        count = dst_mod.write(out, items, force=args.force)
    except FileExistsError:
        print(f"Output file '{out}' already exists. Use --force to overwrite.")
        sys.exit(3)

    print(f"Converted {count} entries from {args.from_fmt} → {args.to_fmt}.")
    print(f"Output written to: {out}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(130)
