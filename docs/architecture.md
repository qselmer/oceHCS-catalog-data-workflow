# Architecture

## Separation of responsibilities

### `qselmer/oceancube`
Reusable software package. It should contain general functions for downloading, reading, extracting, cropping, aggregating, matching, deriving, quality-controlling, and cataloguing multidimensional oceanographic data.

### `qselmer/oceHCS-catalog-data-workflow`
Reusable HCS workflow and catalog. It decides which providers/products/versions/domains are used and records the complete processing and QA/QC trail.

### External HCS data store
Heavy NetCDF/raster/Zarr objects. It is not a Git repository and is not pushed to GitHub.

### Scientific paper repositories
Paper-specific repositories consume subsets of the validated HCS store. They own species observations, paper-specific joins, models, figures, tables, and manuscript files. They should not redownload the master oceanographic archive independently.

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
project-specific extraction
  ↓
paper repositories
```

## Storage principle

Prefer annual or otherwise sensibly chunked NetCDF files for interoperable reusable cubes. Consider Zarr when dataset size, access pattern, or parallel/cloud workflows justify it. Avoid generating one tiny NetCDF per day when a time-chunked cube is more efficient.

## Catalog principle

Every data artifact must be discoverable without opening the binary file. The versioned catalogs therefore record identity, product provenance, coverage, processing level, and checksum separately from the heavy data themselves.
