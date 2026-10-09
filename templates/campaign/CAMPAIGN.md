# Campaign {{NAME}}

Folder: {{DIR}}
Files here: lit_pool/ (shards) + lit_pool.md (merged index) · tree.md · routes.md · barriers.md · results.md ·
ledger.md · runs/ (one file per agent run) · prompts_out/ (generated prompts) · package/ (phase 11+).
To override the budget for this campaign only, put a budget.toml in this folder.

## META
- name: {{NAME}}
- goal_verbatim: {{GOAL}}
- created: {{DATE}}
- project: {{PROJECT}}
- stage: 0-kickoff

## TARGET
- target_status: none
- statement:
- target_value:
- unit:
- better:
- record_value:
- chain:
- model:
- sensitivity:
- ladder:
- quant_runs:
- crosscheck:

```
Field guide for TARGET (filled in phase 2; this fenced block is ignored by the scripts):
- target_status: none -> cross-checked (coordinator compared Q1/Q2 link by link) -> confirmed (user saw it in phase 5)
- statement / target_value / unit / better (higher|lower): the ONE normalised number every route reports against
- record_value: current record converted to the same unit
- chain: user goal -> ... -> target, one arrow per link (e.g. c <= 1.20 -> inequality Z at k = 12 -> delta >= 0.031)
- model: code path + which known record it reproduces (calibration)
- sensitivity: component: improvement needed alone (e.g. "short-range exponent: -0.004; long-range constant: +0.02")
- ladder: milestone: needed value (e.g. "c <= 1.22: 0.018; c <= 1.20: 0.031; c <= 1.18: 0.047")
- crosscheck: per link agree/disagree + how each disagreement was resolved
```

## Stage log
- {{DATE}} 0-kickoff: campaign created

## User decisions
