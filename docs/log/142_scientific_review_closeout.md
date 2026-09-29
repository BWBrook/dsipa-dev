# 142 — Scientific review close-out (18 September 2026)

Fable's board message 225 closes the scientific review tranche and regards the
manuscript as a submission candidate. Barry relayed that verdict here. Astra
read the complete board sequence through 225 and replied in message 230.

Three small text changes were made within the existing authorised manuscript
revision: spell out first-positive annual observations in the abstract; state
the complementary 0.32% eligible-area share in Results 3.1; and report the
matched negative-slope band comparison in 3.3. The abstract did not contain the
37.6% area figure, so no replacement of that statistic was needed there.

The area calculation uses the existing upper two terciles: 5,485.671630676 /
1,710,860.241786434 × 100 = 0.3206382086%, across 280 reserves. The 0.04 product
unit/year division describes this dataset's tercile membership; it is not an
ecological-effect threshold and is not called ‘more than marginal brightening’.
Seven matched whole-negative reserves have negative outer-band slopes: six
zero and one negative deeper-band slope. These are bounded spatial-support
observations. No inference that seven whole-positive/both-band-zero cases must
originate beyond 5 km is added; median pairwise slopes are nonadditive.

Existing tables were read locally for arithmetic/sign tabulation; no new model,
national extraction or raw-raster calculation was run. Input hashes and exact
values are in `analysis/reports/product_closeout_arithmetic.json`; the reasoning
is in `analysis/reports/product_closeout_review.md`.

The main PDF/DOCX was rebuilt and affected native/LibreOffice-rendered pages
were inspected, including abstract, Results, declarations and Table 1. SI is
unchanged and retains its earlier complete visual review. Both build manifests
and all 12 embedded image hashes match current sources. Main PDF/Word render
remains 21/27 pages; SI 20/23. Microsoft Word itself was not tested. The prior
121 passing tests and seven absent-large-input skips are carried forward; no
code behaviour changed, so the full suite was not rerun. Wheel/sdist were
rebuilt to include current repository documentation. Source word counts are
237 abstract + 3,887 body/declarations = 4,124 words.

Current private bundle: `build/final_read/audit_20260918_closeout/` and
`build/final_read/dsipa_rsec_audit_20260918_closeout.zip`. Canonical snapshot:
`artefacts/rsec_audit_20260918_closeout/`. Earlier bundles are preserved.
Validation receipt: `analysis/reports/product_closeout_validation.json`.

No scientific request remains in this tranche. Barry's own full read, author
metadata/declarations/AI disclosure and release decisions remain. The curated
public repository/software record and dataset update with audit source tables
are recommendations, not authorised publication actions. No commit, push,
public deposit or submission was made.
