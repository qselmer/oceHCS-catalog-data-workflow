# Architecture

## Separation of responsibilities

### `qselmer/oceancube`

Reusable software package for downloading, reading, extracting, cropping, aggregating, matching, deriving, quality-controlling, and cataloguing multidimensional oceanographic data.

### `qselmer/oceHCS-environmental-data-workflow`

Reusable Humboldt Current System workflow and environmental catalog. It freezes provider/product/version choices, geographic domains, variable definitions, processing rules, quality-control decisions, and provenance required to reconstruct certified environmental products.

### External HCS data store

Heavy NetCDF, GeoTIFF, Zarr, HDF5, GRIB, and related data objects. This store is not a Git repository and is not pushed to GitHub.

### Scientific paper repositories

Paper-specific repositories consume certified subsets of the HCS store. They own species observations, paper-specific joins, models, figures, tables, and manuscript files. They should not independently redownload or rebuild the master environmental archive unless a deliberately different product or processing contract is part of the study design.

## Data lineage

```text
provider
  ↓
cin/raw/                    immutable original
  ↓
oceancube + frozen config
  ↓
cin/interim/                standardized / derived intermediate
  ↓
QC and provenance gates
  ↓
cin/processed/              reusable analytical products
  ↓
versioned catalog
  ↓
project-specific extraction
  ↓
paper / workflow repositories
```

## Storage principle

Prefer annual or otherwise sensibly chunked NetCDF files for interoperable reusable cubes. Consider Zarr when dataset size, access pattern, parallel execution, or cloud workflows justify it. Avoid one tiny NetCDF file per day when a time-chunked cube is more efficient.

The raw provider artifact is immutable. Standardization, regridding, temporal aggregation, derived variables, climatologies, and anomalies create new artifacts with explicit provenance.

## Catalog principle

Every reusable data artifact must be discoverable without opening the binary file. Versioned catalogs therefore record identity, product provenance, processing level, spatial/temporal support, status, and checksum separately from the heavy data themselves.

`config/*.yml` defines scientific intent and frozen processing contracts. `catalog/*.csv` records certified products and artifacts produced under those contracts. See [`catalog-contract.md`](catalog-contract.md).
