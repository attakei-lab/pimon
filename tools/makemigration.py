#!/usr/bin/env python
"""Shortcut for creating migrations."""
import argparse
import tempfile
from pathlib import Path

from pimon.db import migrations

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("--name", type=str)


def main(args: argparse.Namespace):  # noqa: D103
    db_path = Path(tempfile.mktemp(".sqlite"))
    ctx = migrations.MigrationContext.new(db_path)
    ctx.verbose = args.verbose
    ctx.create(args.name)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
