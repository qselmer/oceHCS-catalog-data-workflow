#!/usr/bin/env python3
"""Validate lightweight repository contracts without touching the external data store."""

from __future__ import annotations

import csv
import hashlib
import os
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "repo.yml",
    "CITATION.cff",
    "VERSION",
    "_quarto.yml",
    "index.qmd",
    "assets/images/logo.svg",
    "config/domain.yml",
    "config/products.yml",
    "config/variables.yml",
    "config/processing.yml",
    "config/paths.example.yml",
    "catalog/products.csv",
    "catalog/variables.csv",
    "catalog/files.csv",
    "catalog/coverage.csv",
    "catalog/checksums.csv",
    "docs/architecture.md",
    "docs/catalog-contract.md",
]

YAML_FILES = [
    "repo.yml",
    "CITATION.cff",
    "_quarto.yml",
    "config/domain.yml",
    "config/products.yml",
    "config/variables.yml",
    "config/processing.yml",
    "config/paths.example.yml",
    "metadata/schemas/products.schema.yml",
    "metadata/schemas/variables.schema.yml",
    "metadata/schemas/files.schema.yml",
    "metadata/schemas/coverage.schema.yml",
    "metadata/schemas/checksums.schema.yml",
]

SCHEMAS = [
    "metadata/schemas/products.schema.yml",
    "metadata/schemas/variables.schema.yml",
    "metadata/schemas/files.schema.yml",
    "metadata/schemas/coverage.schema.yml",
    "metadata/schemas/checksums.schema.yml",
]

HEAVY_SUFFIXES = {
    ".nc", ".nc4", ".grib", ".grb", ".grib2", ".tif", ".tiff",
    ".hdf", ".h5", ".hdf5", ".zarr",
}

SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def fail(message: str) -> None:
    raise AssertionError(message)


def load_yaml(relpath: str):
    with (ROOT / relpath).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def check_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def check_yaml() -> None:
    for relpath in YAML_FILES:
        try:
            load_yaml(relpath)
        except Exception as exc:
            fail(f"Invalid YAML in {relpath}: {exc}")


def check_version_consistency() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    repo = load_yaml("repo.yml")
    citation = load_yaml("CITATION.cff")
    repo_version = str(repo["repository"].get("version", "")).strip()
    citation_version = str(citation.get("version", "")).strip()
    if version != repo_version:
        fail(f"VERSION ({version}) != repo.yml version ({repo_version})")
    if version != citation_version:
        fail(f"VERSION ({version}) != CITATION.cff version ({citation_version})")


def check_catalog_schema(schema_path: str) -> None:
    schema = load_yaml(schema_path)
    table_path = ROOT / schema["table"]
    expected_columns = list(schema["columns"])
    primary_key = schema["primary_key"]
    required = set(schema.get("required", []))
    allowed_status = set(schema.get("allowed_status", []))

    with table_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        observed = reader.fieldnames or []
        if observed != expected_columns:
            fail(
                f"Header mismatch in {schema['table']}: "
                f"expected {expected_columns}, observed {observed}"
            )
        rows = list(reader)

    seen = set()
    for row_number, row in enumerate(rows, start=2):
        key = (row.get(primary_key) or "").strip()
        if not key:
            fail(f"Blank primary key {primary_key} in {schema['table']} row {row_number}")
        if key in seen:
            fail(f"Duplicate {primary_key}={key!r} in {schema['table']}")
        seen.add(key)

        for field in required:
            if not (row.get(field) or "").strip():
                fail(f"Blank required field {field} in {schema['table']} row {row_number}")

        status_field = "qc_status" if "qc_status" in row else "status" if "status" in row else None
        if status_field and allowed_status:
            status = (row.get(status_field) or "").strip()
            if status and status not in allowed_status:
                fail(
                    f"Invalid {status_field}={status!r} in {schema['table']} row {row_number}; "
                    f"allowed: {sorted(allowed_status)}"
                )

        if "relative_path" in row:
            rel = (row.get("relative_path") or "").strip()
            if rel:
                if PurePosixPath(rel).is_absolute() or PureWindowsPath(rel).is_absolute():
                    fail(f"Absolute path in {schema['table']} row {row_number}: {rel}")
                if re.match(r"^[A-Za-z]:[\\/]", rel):
                    fail(f"Machine-specific Windows path in {schema['table']} row {row_number}: {rel}")

        if "sha256" in row:
            digest = (row.get("sha256") or "").strip()
            if digest and not SHA256_RE.fullmatch(digest):
                fail(f"Invalid SHA-256 in {schema['table']} row {row_number}")

        if "algorithm" in row and "checksum" in row:
            algorithm = (row.get("algorithm") or "").strip().lower()
            digest = (row.get("checksum") or "").strip()
            if algorithm == "sha256" and digest and not SHA256_RE.fullmatch(digest):
                fail(f"Invalid SHA-256 checksum in {schema['table']} row {row_number}")


def check_catalogs() -> None:
    for schema_path in SCHEMAS:
        check_catalog_schema(schema_path)


def check_no_heavy_files() -> None:
    offenders = []
    ignored_roots = {".git", "_site", ".quarto", "_freeze"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in ignored_roots:
            continue
        lower_name = path.name.lower()
        if path.suffix.lower() in HEAVY_SUFFIXES or lower_name.endswith(".zarr"):
            offenders.append(rel.as_posix())
    if offenders:
        fail("Heavy environmental files committed to repository: " + ", ".join(offenders))


def main() -> int:
    checks = [
        ("required files", check_required_files),
        ("YAML", check_yaml),
        ("version consistency", check_version_consistency),
        ("catalog schemas", check_catalogs),
        ("heavy-file policy", check_no_heavy_files),
    ]

    for name, check in checks:
        check()
        print(f"PASS: {name}")

    print("Repository validation: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(f"Repository validation: FAIL\n{exc}", file=sys.stderr)
        sys.exit(1)
