# Local data mount

This directory is only a placeholder documenting the relationship between the Git repository and the heavy oceanographic data store.

Do **not** place version-controlled scientific data here.

Configure the external data root in:

```text
config/paths.local.yml
```

Example:

```yaml
ocean_data_root: "D:/oceHCS-data"
```

The external store must use:

```text
D:/oceHCS-data/
├── cin/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── metadata/
└── cout/
    ├── qc/
    ├── reports/
    └── logs/
```

`cin/raw/` is immutable. Processed/interim artifacts are reproducible from raw inputs plus versioned workflow code and configuration.
