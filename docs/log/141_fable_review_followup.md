# 141 — Fable review follow-up (18 September 2026)

Barry relayed Fable's review of the September 17 audit and manuscript. The
follow-up addresses correspondence messages 207–208, preserving the accepted
national extraction, original audit protocol and previous reading bundles.
New diagnostic extensions are explicitly exploratory after result inspection.

## Results and manuscript changes

- Reproduced the 64/78 first detections in 2023–2024 and onset-year persistence.
  The abstract/Results now report the 2017 pulse and synchronous 2023 increases;
  no 2022 spike is not reassurance about continuity. Buffer and pixel-transition
  dip/rebound patterns admit a processing explanation without identifying it.
- Scanned remaining 2014–2019 raster windows on deep-server. The minimum
  positive decoded pixel value is 10 across all 2013–2024 windows. Five
  higher-value off-lattice pixels do not affect the floor. Means can be below
  10, physical conversion is unverified, and separate masking/encoding
  contributions to the zero mass remain unidentified.
- Added 0–1 km slopes on exactly the prior 1,205-reserve matched cohort. Among
  119 positive-whole cases, 79 have positive outer-band and zero deeper-band
  slopes; 30 are positive in both. All 68 Q1 losses have zero deeper slopes,
  but only 54 have all-zero annual histories. Fourteen contain positive values.
- The lowest count-based tercile of 420 positive whole-reserve slopes contains
  99.147% of positive-class summed polygon area. The 37.6% eligible-area
  share is now explicitly qualified by magnitude and whole-polygon assignment.
- Added generated Table S5 for tercile magnitude/area and matched-band signs.
  Figure S8 uses separate zero-based distance panels and marked calendar years.
  Folded the Layer B Results paragraph into 3.3, removed redundancy, renamed
  Table 1's count-percentage header and expanded Data accessibility.

## Review and verification

Independent claim review corrected overly definite attribution of zeros to
quantisation and narrowed ‘2023 pulse’ to ‘2023 increases’ because inside
first detections remain elevated in 2024. Independent numerical review
reproduced the cohort, area and sign counts, and caught a source/output mismatch
during script finalisation. The final edge analysis was rerun and its local and
remote source hash matches the execution manifest.

Remote scratch roots:
- `/data/codex/scratch/dsipa-product-floor-20260918/`
- `/data/codex/scratch/dsipa-edge-followup-20260918/`

Both used persistent tmux sessions and accepted inputs read-only. No raw-data
replacement, full national rerun, or external-product acquisition was needed.
New generated output directory `analysis/reports/edge_followup/` follows the
existing report convention and is referenced in README and handover.

Validation: 121 tests passed, seven skipped for absent local large inputs;
four targeted edge tests also passed after finalisation. Python wheel/sdist
built. Both makedoc profile checks and final builds passed. Current source and
output hashes match both document build manifests; all four main and eight SI
embedded image hashes match source figures. Native PDFs and LibreOffice DOCX
renders were inspected, including Table 1, Table S5 and Figure S8. Microsoft
Word itself was not tested. An isolated declaration page was removed by
using compact bold declaration labels, then affected pages were rechecked. Main PDF/Word render: 21/27 pages; SI: 20/23.
Main source count: 234 abstract + 3,826 body/declarations = 4,060 words.

## Deliverables and boundaries

Primary follow-up report: `analysis/reports/product_followup_review.md`.
Execution evidence: `product_floor_*`, `product_onset_persistence.csv`,
`product_pulse_followup_manifest.json`, and `edge_followup/`.
Validation receipt: `analysis/reports/product_followup_validation.json`.
Private reading bundle: `build/final_read/audit_20260918/` and
`build/final_read/dsipa_rsec_audit_20260918.zip`.
Canonical source/evidence receipt: `artefacts/rsec_audit_20260918/`.

Board replies 214 and 216 report the correction and new evidence. The paper
retains product-level conservation-screening claims. Environmental onset,
lighting sources and spillover remain unidentified. Final author metadata,
declarations/AI disclosure, public code release and submission remain Barry's
decisions. No commit, push, public deposit or submission was made.
