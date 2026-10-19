# DSIPA AI model inventory — 19 October 2026

Read-only project-specific reconnaissance; no model identities inferred from
current role definitions. The main declaration lists all seven recoverable
labels. Supporting Methods S6 records roles, dates and limits. This replaces
R3's overly broad September–October attribution to generic GPT-6 and Opus 5.5.

## Evidence

- `docs/log/000_bootstrap.md:5–7`: 1 January 2026, Codex CLI (GPT-5),
  environment/scaffold and initial study planning. No finer backend identifier.
- Legacy Codex state database `threads` rows
  `019cc0df-5d36-71d0-94bc-12d510635fff` (created 6 March, last updated 25 May)
  and `019e2949-c550-71f0-923e-dddd0af30736` (15 May): `gpt-5.5`, xhigh.
  The former concerns environment/bootstrap; the latter manuscript expansion
  and formatting. Registered archived JSONL paths are absent. Model fields
  identify retained assignments, not all turns.
- DSIPA parent session `01a093eb-cee1-7c31-b08a-fdf98d855eef`: all 25
  inspected turn-context records name `gpt-6-astra`. Records at JSONL lines 8
  and 5638 are high effort (12 and 19 September); lines 5689 and 7522 are xhigh
  (18 and 19 October). Parent spawn records at lines 2776 and 4268 name
  `gpt-6-astra/max` for independent review. Log 143:11–13 corroborates the
  fresh September 18 adversarial review. October linked child sessions also
  record `gpt-6-astra/xhigh`.
- The active Codex state database was queried read-only and restricted to
  this exact repository cwd. September specialist assignments are listed below;
  their registered child JSONL files are absent. Parent dates and task identities
  survive, but full per-turn histories do not.
- `analysis/reports/editorial_claude_r3_review_20261019.md:63–73` and board 90
  message 2063: explicit Claude-reported Fable 5.1/Opus 5.5 dates and roles.
  Commit trailers 59725d3, 2a7982c and 77af011 corroborate Opus 5.5; September 28 start
  and Fable identity are collaborator reports, not Anthropic metadata audits.

## September specialist assignments

| Date | Task | Model | Record ID |
| --- | --- | --- | --- |
| 12 Sep | methods_orientation | gpt-5.6-sol | 01a093ec-99b2-7191-aba5-355486563fbb |
| 12 Sep | figures_revision | gpt-5.6-luna | 01a09400-9e55-79a3-949f-9e8499ae6a6a |
| 17 Sep | interior_audit | gpt-5.6-luna | 01a0adf5-f388-7be3-b55a-212ee68aebe6 |
| 17 Sep | audit_design_review | gpt-5.6-sol | 01a0adf6-1ff4-7540-8000-9df9aec135d4 |
| 17 Sep | product_lineage | gpt-5.6-sol | 01a0adf6-c2d2-71d1-b7b5-eae67186c851 |
| 19 Sep | coastline_source_selection | gpt-5.6-sol | 01a0b7ff-9d3b-7342-9b99-9cb71e63bb82 |
| 19 Sep | layerb_review_repairs | gpt-5.6-luna | 01a0b7ff-dec1-74b2-82a5-2fe88a751966 |
| 19 Sep | release_input_reconciliation | gpt-5.6-luna | 01a0b800-3636-7351-8509-ef878b3a33f3 |
| 19 Sep | spatial_protocol_check | gpt-5.6-sol | 01a0b807-7c05-7631-ad56-a78dd01e2760 |
| 19 Sep | corrected_audit_orchestration | gpt-5.6-luna | 01a0b80d-5f50-7943-a805-99ea0337c3b9 |
| 19 Sep | corrected_figure_table_plumbing | gpt-5.6-luna | 01a0b819-8e27-7831-b294-39736c721f89 |

## Limits

The precise initial GPT-5 variant, exhaustive January–early September model
history and identity of the earlier ChatGPT PI-review workflow are unresolved.
This is a documented provenance limit, not a claim that those systems were
unused or that current versions were used historically. The main declaration
and SI make known roles explicit without calling the inventory exhaustive.
No unrelated conversations, credentials or raw private transcripts are included.
