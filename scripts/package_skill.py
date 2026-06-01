#!/usr/bin/env python3
"""Package and validate the thesis-figure-skill .skill archive.

By default this script rebuilds thesis-figure-skill.skill from the complete
skills/thesis-figure-skill directory. In pull requests, prefer writing to a
temporary output path (for example /tmp/thesis-figure-skill.skill) so the PR
stays source-only and does not include an unsupported binary archive diff.
Use --check to verify an already-built archive matches the source tree exactly.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

DEFAULT_SKILL_DIR = Path("skills/thesis-figure-skill")
DEFAULT_OUTPUT = Path("thesis-figure-skill.skill")
FIXED_ZIP_TIMESTAMP = (2024, 1, 1, 0, 0, 0)
IGNORED_PARTS = {"__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo", ".DS_Store"}


def iter_skill_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(skill_dir)
        if any(part in IGNORED_PARTS for part in rel.parts):
            continue
        if path.name in IGNORED_SUFFIXES or path.suffix in IGNORED_SUFFIXES:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(skill_dir).as_posix())


def build_archive(skill_dir: Path, output: Path) -> None:
    if not (skill_dir / "SKILL.md").is_file():
        raise SystemExit(f"SKILL.md not found in {skill_dir}")

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in iter_skill_files(skill_dir):
            rel = path.relative_to(skill_dir).as_posix()
            info = zipfile.ZipInfo(rel)
            info.date_time = FIXED_ZIP_TIMESTAMP
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o644 & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())


def check_archive(skill_dir: Path, output: Path) -> int:
    if not output.is_file():
        print(f"ERROR: archive not found: {output}", file=sys.stderr)
        return 1

    source_files = iter_skill_files(skill_dir)
    expected = {path.relative_to(skill_dir).as_posix(): path.read_bytes() for path in source_files}

    with zipfile.ZipFile(output) as archive:
        actual_names = sorted(name for name in archive.namelist() if not name.endswith("/"))
        expected_names = sorted(expected)
        missing = sorted(set(expected_names) - set(actual_names))
        extra = sorted(set(actual_names) - set(expected_names))
        mismatched = sorted(
            name for name in set(actual_names) & set(expected_names) if archive.read(name) != expected[name]
        )

    if missing or extra or mismatched:
        print("ERROR: .skill archive does not match skill directory", file=sys.stderr)
        if missing:
            print("Missing from archive:", *missing, sep="\n  ", file=sys.stderr)
        if extra:
            print("Extra in archive:", *extra, sep="\n  ", file=sys.stderr)
        if mismatched:
            print("Content mismatches:", *mismatched, sep="\n  ", file=sys.stderr)
        return 1

    print(f"OK: {len(expected_names)} files match {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="verify instead of rebuilding")
    args = parser.parse_args()

    skill_dir = args.skill_dir
    output = args.output

    if args.check:
        return check_archive(skill_dir, output)

    build_archive(skill_dir, output)
    return check_archive(skill_dir, output)


if __name__ == "__main__":
    raise SystemExit(main())
