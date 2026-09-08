# Contributing

Contributions should preserve the separation between reusable software, scientific workflow configuration, catalog records, and heavy external data.

Before proposing a change:

1. do not commit NetCDF, GeoTIFF, Zarr, HDF5, GRIB, credentials, or machine-specific paths;
2. update `config/*.yml` when changing scientific intent or processing rules;
3. update `catalog/*.csv` only for reviewed or generated catalog records;
4. preserve provider/product/version provenance and checksums;
5. document derived-variable dependencies explicitly;
6. run `python tests/validate_repository.py` locally after installing `pyyaml`;
7. ensure the Quarto site renders successfully.

Changes that alter the master HCS domain, provider products, variable definitions, or processing algorithms should include a documented scientific rationale in the corresponding `workflow/*.qmd` file.
