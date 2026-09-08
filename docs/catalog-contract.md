# Catalog contract

## Purpose

The repository separates scientific configuration from certified artifact records.

- `config/*.yml` defines the intended domain, products, variables, processing rules, and local path contract.
- `catalog/*.csv` records products and artifacts that have actually been reviewed or generated under those rules.
- `metadata/schemas/*.yml` defines the required columns, key fields, and validation rules for each catalog table.

The configuration and catalog layers are not duplicate sources of truth.

## Direction of information

```text
scientific review
  ↓
config/*.yml
  ↓
acquisition / processing / QC
  ↓
catalog/*.csv
  ↓
validation against metadata/schemas/*.yml
  ↓
GO / REVIEW / STOP
```

## Catalog tables

### `products.csv`

One row per provider product/version used by the workflow. `product_key` is the primary key.

### `variables.csv`

Canonical variables and declared derived-variable dependencies. `variable_key` is the primary key and `product_key` links provider-backed variables to `products.csv`.

### `files.csv`

One row per external heavy-data artifact. Paths must be relative to the configured external data root. `file_key` is the primary key.

### `coverage.csv`

Spatial/temporal support and missingness diagnostics for a product-variable-domain interval. `coverage_key` is the primary key.

### `checksums.csv`

Checksum verification records for external artifacts. `file_key` should resolve to `files.csv` when the corresponding artifact has been catalogued.

## Validation rules

At minimum, automated validation must verify:

1. exact catalog headers;
2. unique non-empty primary keys;
3. relative rather than machine-specific absolute paths;
4. valid SHA-256 strings when checksums are populated;
5. declared status values;
6. parseable configuration and schema YAML;
7. absence of heavy binary products from Git history.

Referential integrity and richer semantic checks should be added as real catalog records are populated.

## Release principle

A downstream scientific repository should record the catalog release or commit it consumed. Certified releases should freeze the domain, product versions, variable definitions, processing rules, catalog manifests, checksums, and relevant `oceancube` version.
