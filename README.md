# oceHCS-catalog-data-workflow

Reproducible workflow for the acquisition, quality control, harmonization, derivation, cataloguing, and reuse of oceanographic and environmental data across the Humboldt Current System (HCS), with initial support for Peru and Chile.

> **Repository type:** `type-methods-workflows`
>
> **Primary software engine:** [`qselmer/oceancube`](https://github.com/qselmer/oceancube)
>
> **Heavy data policy:** NetCDF, GeoTIFF, Zarr, HDF5, GRIB, and other large rasters are stored outside GitHub in a local/external data lake and are referenced through versioned catalogs, manifests, checksums, and provenance records.

## Purpose

This repository provides a reusable data workflow for projects that require environmental covariates from the Humboldt Current System. It is designed to avoid downloading and processing the same oceanographic products independently for every paper, stock, species, or analysis.

The workflow separates three layers:

1. **Software** — `oceancube` implements reusable download, extraction, harmonization, derivation, QA/QC, and catalog functions.
2. **Workflow and catalog** — this repository records what products are used, how they are processed, which domains are supported, and how provenance is tracked.
3. **Heavy data store** — the actual NetCDF/raster/Zarr products live outside GitHub and are linked locally through `config/paths.local.yml`.

## Initial scientific domain

The master domain is the Humboldt Current System rather than a single Peruvian stock. It is intended to support, among others:

- Peruvian anchoveta North-Central stock;
- Peruvian/Chilean southern anchoveta analyses;
- jack mackerel, chub mackerel, sardine, and other pelagic species;
- community and ecosystem analyses;
- fleet-distribution and climate-risk studies;
- recruitment, habitat, SDM/ENM, MSE, and stock-assessment covariates.

The exact geographic extent is controlled in `config/domain.yml` and must be scientifically frozen before bulk acquisition.

## Data architecture

```text
oceHCS-catalog-data-workflow/
├── config/                 # versioned contracts and local-path template
├── R/                      # workflow helpers built around oceancube
├── workflow/               # Quarto audit trail, one step at a time
├── catalog/                # versioned products/files/coverage/checksums
├── metadata/               # provenance, schemas, licences
├── tests/                  # workflow tests
├── docs/                   # architecture and data contracts
└── local/                  # local mount placeholder; heavy data ignored
```

The external data lake follows the canonical scientific layout:

```text
<oceHCS_data_root>/
├── cin/
│   ├── raw/                # original immutable provider files
│   ├── interim/            # standardized or partially harmonized products
│   ├── processed/          # reusable analytical cubes/layers
│   └── metadata/           # provider-side metadata and provenance
└── cout/
    ├── qc/
    ├── reports/
    └── logs/
```

## Core candidate variables

The catalog is designed to support, when scientifically justified:

- SST;
- SSS;
- mixed-layer depth;
- dissolved oxygen and oxycline diagnostics;
- chlorophyll-a and primary productivity;
- sea-surface height / absolute dynamic topography;
- currents and EKE;
- wind, wind stress, alongshore stress, Ekman/upwelling diagnostics;
- bathymetry, coastline, and distance to coast;
- additional fronts, gradients, or climate products when required.

Native source resolution is preserved. Regridding never replaces the raw product.

## Quality-control principle

The workflow follows:

```text
DOMAIN
  ↓
PRODUCT REGISTRY
  ↓
ONE VARIABLE AT A TIME
  ↓
SOURCE QC
  ↓
MATCHING / HARMONIZATION QC
  ↓
COVERAGE BY TIME × SPACE
  ↓
GO / REVIEW / STOP
  ↓
NEXT VARIABLE
```

A high global coverage percentage is never sufficient by itself. Coverage is audited by time block, spatial domain, product, and downstream scientific unit so that an entire survey/event cannot silently disappear from later complete-case analyses.

## Local setup

Copy:

```text
config/paths.example.yml
```

to:

```text
config/paths.local.yml
```

and set your local heavy-data root, for example:

```yaml
ocean_data_root: "D:/oceHCS-data"
```

`config/paths.local.yml` is ignored by Git.

## Repository metadata

Recommended GitHub description:

> Reproducible workflow and catalog for acquisition, QC, harmonization, derivation, and reuse of oceanographic data across the Humboldt Current System using oceancube.

Recommended topics:

`type-methods-workflows`, `oceanography`, `humboldt-current-system`, `peru`, `chile`, `ocean-data`, `copernicus-marine`, `era5`, `netcdf`, `zarr`, `oceancube`, `reproducible-research`, `species-distribution-models`, `fisheries`

## Status

Initial infrastructure and data-governance setup. No bulk environmental download should begin until the domain and product registry are frozen.
