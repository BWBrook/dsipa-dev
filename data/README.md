# Data inventory

Record every dataset placed under `data/raw/` and the derived products under `data/processed/`.

| Name | Source URL / DOI | Version / date fetched | License | Checksum (e.g., sha256) | Notes |
| --- | --- | --- | --- | --- | --- |
| _[fill]_ | _[fill]_ | _[fill]_ | _[fill]_ | _[fill]_ | _[processing steps / quirks]_ |

Rules:
- Do not hand-edit files in `data/raw/`; recreate via scripts.
- Store scripts used for downloads/processing in `src/` or `analysis/` and reference them here.
- If data cannot be redistributed, keep it out of git and document the retrieval steps instead.
