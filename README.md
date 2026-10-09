# research-campaign

A Claude Code skill for running **multi-agent math research campaigns** (pushing a record or an explicit bound,
improving a constant, attacking a lemma chain, certifying a computation) with cheap gates in front of every
expensive step.

It was built from the retrospective of a real multi-agent campaign, where most of the waste was decidable in
advance: attacks whose ideal ceiling was below the target, obstructions already stated in a cited paper, borrowed
theorems whose hypotheses did not match, duplicated routes, a record that had already been posted on a faculty
page, and results checked four times while unchecked relayed claims held the real errors.

## What it does

A 15-phase pipeline, with scripts that enforce the rules mechanically:

1. **Kickoff** with a user-owned budget (agents, memory).
2. **Literature pool**: a rough sweep, then verifiers by source class, then close reading; target-string search,
   personal pages, a sweep of AI/computational-discovery papers' full texts, and released artifacts
   (constructions, code) recorded for reuse.
3. **Target quantification** by two blind agents with different methods, cross-checked link by link; the
   sensitivity table is in the record method's own parameters.
4. **AND/OR problem tree** with small, numerically targeted leaves; a **tool hunt** per bottleneck node.
5. **Route cards** and an **ideal-ceiling gate** (GO / KILL / CONJ / UNCERTAIN → scout) before any attack.
6. **Launch gate** (`check_launch.py`): budget, target status, complete cards, dedup by method class and
   deliverable, killed-class relaunch rules, per-node limits, stale-prompt hash.
7. **Attacks** with content-based return conditions (no time caps).
8. **One independent check per result version** (a registry refuses a second check).
9. **Stop rule** (root blocked, or one barrier blocking three method classes).
10. **Freeze → one final audit → paper + Lean tracks → delivery.** Nothing is published without the user.

## Install

Copy this folder to `~/.claude/skills/research-campaign/` (all projects) or to `<project>/.claude/skills/` (one
project). Requirements: Claude Code with subagents, web search/fetch, a shell, and Python 3.11+ (stdlib only).
Lean 4 + Mathlib and a TeX engine are optional.

## Configure (all optional, all yours)

Create these next to `SKILL.md`; they override the shipped defaults and are never written by Claude:

```toml
# config.local.toml
python        = "/usr/bin/python3"        # interpreter for the scripts
projects_root = "/home/me/research"       # where project folders live
lean_bin      = ""                        # folder with lean/lake if not on PATH
mathlib_cache = ""                        # local Mathlib cache, if any
typesetting   = ""                        # HTML math renderer when no TeX engine exists
```

```toml
# budget.local.toml
max_concurrent_agents  = 4
total_memory_gb        = 16
per_agent_memory_gb    = 6
max_active_per_or_node = 2
```

A campaign can override the budget again with its own `budget.toml`.

## Use

Ask Claude in your own words, e.g. "start a campaign to beat the record for X", "resume the campaign", "push this
bound below 1.2". The skill creates `campaigns/<date>-<slug>/` in your project folder, with card files
(`CAMPAIGN.md`, `tree.md`, `routes.md`, `barriers.md`, `results.md`, `ledger.md`, `lit_pool/`) that the scripts
read and update. For a single-agent task under about 30 minutes it runs a light mode without the campaign files.

Run `python -I tests/selftest.py` after changing any script.

## Results

On long multi-agent campaigns the skill saves **roughly 20% of subagent tokens**. In a blind replay of a real
campaign window (30 launches, 3.7 hours, 9.7M tokens), the gate killed 7 launches, all correctly, for an 18.5%
net saving after its own cost. Scouts and deferrals were counted as zero saving, so this is conservative.

As a regression suite we also built 203 synthetic launch-gate cases with one seeded fault each (17 fault types,
12 areas of mathematics). With Sonnet 5.5 as the gate, 97% of verdicts were right, with no false kills and no
false passes; the reason category also matched in 89%.

## Problems we found

1. **A wrongful merge.** The gate merged a launch that shared some reading with another run but delivered
   something different (calibrated numbers the next phase relied on). Fixed: dedup compares deliverables, and a
   partial overlap is trimmed, not merged. The re-test passed.
2. **Results hidden in a paper's body are missed.** A scoop that appeared only inside a machine-learning paper,
   whose abstract never names the problem, was missed in every run. A "methods-paper sweep" was added, but agents
   still skipped it in re-tests, so this is an **open problem**.
3. **No saving on short tasks.** On ~30-minute single-agent tasks the skill costs 18-37% more tokens (about 15k
   tokens of reading). A light mode without campaign files was added for that size.
4. **Confirming what a theorem already settles.** An agent ran a solver for 7 minutes after a published theorem
   had already ruled the target out. Fixed: a KILL backed by a theorem is final.
5. **Targets too coarse.** Target quantification stopped at the goal's own unit ("need size 368") instead of the
   record method's parameters (which part of the record construction must improve). Fixed in the quantification
   prompt.
6. **Ambiguous handling of a moved record.** In unattended runs one agent stopped at the scoop and another
   retargeted. Now: report it, then retarget to the true record if the ceiling gate passes.
7. **Ignoring released constructions.** Runs that knew the record started from scratch. Now attacks on
   construction records start from the released construction or code.
8. **Checks deferred for off-path results.** Fixed: every result gets its one check when it is registered.
9. **Weaker models as gates.** Haiku follows explicit rules well but is noisy as a gate on real research
   transcripts and searches literature shallowly; use a stronger model for gating and literature.
10. **"Wait" chosen over "scout" or "trim".** Four of the six misses on the seeded suite were DEFER where the
    answer was a ceiling scout or a trimmed launch. Nothing is wasted, but the useful part starts later. (Of the
    other two, one was a case with wrong numbers that the gate itself caught, and one was MERGE instead of KILL.)
11. **The stop rule is noticed per route, not per campaign.** When one barrier already blocked three method
    classes, the gate killed the fourth route every time but named the campaign stop rule in only 5 of 12 cases.
    `status.py` and `tree_status.py` raise this signal mechanically; rely on them, not on the gate's prose.
12. **Evaluation limits.** The replay is in-sample (the skill was built from the same campaign) and covers one
    window; the seeded cases are synthetic and were written and judged by the same model family. The numbers are
    indicative, not a benchmark.

## Files

- `SKILL.md`: the pipeline, standing rules and user touchpoints.
- `references/`: one file per phase group (literature, target and tree, routes and attack, closing).
- `prompts/`: templates for every subagent kind; `scripts/make_prompt.py` fills them from the campaign state.
- `scripts/`: `init_campaign`, `status`, `make_prompt`, `check_launch`, `finish_run`, `result`, `merge_pool`,
  `tree_status`, `rclib`.
- `templates/campaign/`: the card files a new campaign starts from.
- `tests/selftest.py`: end-to-end test of every gate on a throwaway campaign.
- `config.toml`, `budget.toml`: shipped defaults (override with the `.local.toml` files).

## License

MIT; see `LICENSE`.
