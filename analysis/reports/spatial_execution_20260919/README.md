# Sealed national extraction evidence

The code snapshot and run/extraction/raster/runtime manifests describe the
completed national_v2 run on 19 September 2026. The runner and engine hashes
match the frozen source files. All 928 chunk receipts and 4,640 part-file hashes
were verified, covering each of 11,133 identifiers exactly once.

Current candidate source has subsequent structural and metadata fixes, described
in the parent protocol and schema amendment. The original buffer-validity CSV
is retained here to verify the added schema_version column without changing
any existing field. All other corrected analytical outputs retain their original
extraction identities. Large raw rasters and chunk payloads remain on deep-server;
their identities and provenance are recorded here.
