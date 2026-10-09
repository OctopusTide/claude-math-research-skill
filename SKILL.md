---
name: research-campaign
description: >-
  Gated orchestration for multi-agent math research campaigns: pushing a record or explicit bound, improving a
  constant, attacking a conjecture or lemma chain, or certifying a computation. It runs a gated pipeline:
  - a kickoff with a user-owned budget;
  - a shared literature pool (a rough sweep, then verification, then close reading);
  - two blind target quantifications cross-checked link by link;
  - an AND/OR problem tree and a tool hunt;
  - route cards with an ideal-ceiling kill gate;
  - scripted launch checks (budget, dedup, stale prompts);
  - attacks with content-based return conditions;
  - a one-check-per-result registry and a stop rule;
  - then freeze, a final audit, and paper + Lean tracks.
  Use it whenever the user starts, resumes or plans a research push that will use subagents, e.g.
  "开个新战役", "继续战役", "把这个界推到新纪录", "改进 X 的下界", "攻这个猜想", "push the bound", "beat the record",
  "certify this", even if they never say "campaign", and before launching any research subagent while a campaign
  exists.
compatibility: >-
  Claude Code with subagents (Agent tool), web search/fetch and a shell. Python 3.11+ (stdlib only) for the
  scripts. Scripts tested on Windows; Linux and macOS supported. Lean 4 + Mathlib and a TeX engine are optional
  (formalisation and paper tracks).
license: MIT
---

# Research campaign

This skill turns the lessons of an earlier multi-agent research campaign into gates. In that
campaign:
- **Cheap pre-checks would have saved ~40% of 6.7M subagent tokens:** one-line ceilings, theorem-hypothesis checks,
  and dedup of overlapping routes.
- **We re-derived a result that was already public.** It had been posted only on a faculty page.
- **Targets arrived after the attacks had launched.**
- **20 JVMs filled the RAM.**
- **One result was checked 4-5 times, while the two real errors were in unchecked claims relayed to the user.**

The scripts enforce the rules mechanically, so they do not depend on the coordinator remembering them.

Reply to the user in their language. Keep agent prompts and campaign files in English (they are working
documents); the scripts print English, and you relay their reports in the user's language.

## Setup

Machine settings live next to this file, all user-owned; Claude reads them and never edits them:
- `config.toml` (shipped, empty) overridden by `config.local.toml`: `python`, `projects_root`, `lean_bin`,
  `mathlib_cache`, `typesetting`;
- `budget.toml` (shipped defaults) overridden by `budget.local.toml`, then by a campaign's own `budget.toml`.

If `config.local.toml` is missing on first use, tell the user which keys exist and that the defaults (PATH tools,
ask for the project folder, the shipped budget) apply until they create it.

```
PY = config `python`, or python3 / python on PATH (>= 3.11, stdlib only); always run it with -I
RC = <this skill's folder>/scripts
PY -I RC/status.py <campaign dir>
```
Commands below are written as `PY -I RC/<script> ...`; use your shell's syntax (in PowerShell: `& $PY -I "$RC\<script>" ...`).

Campaign state lives in `<project>/campaigns/<date>-<slug>/`:
- `CAMPAIGN.md`: META + TARGET cards, stage log, user decisions;
- `lit_pool/` + `lit_pool.md`;
- `tree.md`, `routes.md`, `barriers.md`, `results.md`, `ledger.md`;
- `runs/`: one file per agent;
- `prompts_out/`;
- `package/`.

All of them are Markdown "cards": `## ID title` followed by `- key: value` lines. Edit them with the Edit tool. The
scripts read and update the same fields. Each template's fenced block documents its format.

## The pipeline

| # | phase | who | leaves when | details |
|---|---|---|---|---|
| 0 | kickoff | `init_campaign.py` | user says go (or adjusts goal/budget/inheritance) | below |
| 1 | literature pool | L0 rough sweep → V1..Vk verify + gap fill → R1..Rm close reading | merged pool; scoops reported; stated obstructions registered as barriers | references/literature.md |
| 2 | target quantification | Q1 + Q2, blind, different methods; coordinator cross-checks link by link | TARGET card filled, `target_status: cross-checked` | references/target_and_tree.md |
| 3 | problem tree | coordinator | AND/OR tree; leaves pass the leaf test | references/target_and_tree.md |
| 4 | tool hunt | one agent per bottleneck node (mode A) | candidates in pool → OR branches | references/literature.md |
| 5 | user review | coordinator → user | user OKs target + tree → `target_status: confirmed` | references/target_and_tree.md |
| 6 | route cards | coordinator | one card per OR-branch method | references/routes_and_attack.md |
| 7 | ceiling gate | coordinator (one-liners, barrier lookups) or scouts | verdict GO / KILL / CONJ (user decides) / UNCERTAIN → scout | references/routes_and_attack.md |
| 8 | attack | attack agents, queued by priority within budget | content-based return conditions | references/routes_and_attack.md |
| 9 | check | one designated check per result version | `results.md` check_status passed/failed | references/routes_and_attack.md |
| 10 | loop / stop | `tree_status.py` after every return | root solved → 11; root blocked or barrier convergence → tell the user | references/routes_and_attack.md |
| 11 | freeze | `result.py freeze` + build `package/` | package complete | references/closing.md |
| 12 | final audit | AUD-logic, AUD-num, AUD-lit, fresh agents | all three pass | references/closing.md |
| 13 | paper + Lean | PAPER and LEAN in parallel | draft built; Lean builds with declared axioms | references/closing.md |
| 14 | delivery | coordinator → user | user has it; nothing published without their OK | references/closing.md |

Throughout: barrier-triggered tool hunts (mode B), on-demand literature lookups that write back to the pool, and
claim hygiene. Read the phase's reference file when you enter that phase; the table above is the map.

Record every phase transition as a line in CAMPAIGN.md's stage log, and update META `stage:`.

## Scaling to the size of the campaign

The full pipeline is sized for multi-hour campaigns. For a small one (expected under about an hour, or a single
well-posed computation), keep the ORDER and the GATES but shrink each phase:
- **Literature.** One agent, or the coordinator itself, does sweep and verification together. It still searches
  the explicit target strings, runs the methods-paper sweep (full texts of recent AI/computational-discovery
  papers, see references/literature.md) and checks personal pages and trackers, since that is
  where the scoops were. Close reading covers only the 1-3 sources that set the current record, always including
  the record-setting paper, and notes any released construction or code.
- **Quantification.** There are still two independent computations of the target. One may be the coordinator's
  own and the other a quick agent, or two different methods in the main thread. Cross-check them link by link.
- **Tree.** Often a single node with two or three routes. Run a tool hunt only if every route dies at the ceiling
  gate.
- **Ceiling gate and one-check rule.** Unchanged. They are cheap and they are where small campaigns waste the
  most time: attacking a target that is already beaten, or one that a known bound rules out.
- **Closing.** Freeze + a short audit + a write-up. Lean only if the user asks.

**Single-agent tasks under about 30 minutes** (no subagents at all): skip `init_campaign.py` and the card files.
Keep one `log.md` with a line per gate, in this order: literature (target strings + full text, released
artifacts), target (+ sensitivity in the record method's parameters), ceiling verdict, the one check, and the
scoop decision. At this size the skill's value is in those decisions; the files cost about 15k tokens and half a
minute for nothing.

**Unattended runs.** When the user has pre-authorised the touchpoints (kickoff, budget, target confirmation) in
the task itself, record that under User decisions and continue without waiting.
- **Scoop or moved record** (user decision, 2026-10-09): report it at once in the stage log and the final report,
  then RETARGET to the true record and continue, provided the new target passes the ceiling gate. The user's goal
  is usually "beat the record", not "beat this number". Stop and report instead only if the new target fails the
  ceiling gate, or the goal was tied to the old value or a specific method.
- **Stop-rule verdict:** stop and report it rather than working past it.

In interactive runs a scoop stays a user touchpoint: tell the user at once.

## Phase 0: kickoff

1. From the user's message, get three things: the goal in their exact words (it becomes the search string), the
   project folder (an existing one under config `projects_root`, or a new one), and a short slug. Ask only if the
   project folder is genuinely unclear.
2. Run `PY -I RC/init_campaign.py --project <dir> --name <slug> --goal "<verbatim goal>"`. It creates the
   folder from templates and prints a kickoff report:
   - the budget (budget.toml / budget.local.toml);
   - free RAM against the budget;
   - leftover java/python/lean processes;
   - older campaigns in the same project that could be inherited.
3. Relay the report and WAIT for the user's reply. The goal wording drives the literature search, and the budget
   is theirs. Leftover processes are only reported: never kill processes you did not start without asking.
4. If they want inheritance: `init_campaign.py --dir <campaign> --inherit-from <older campaign>`, then tell L0 to
   sweep only what is newer.

## Launch protocol: every subagent, every phase

1. `PY -I RC/make_prompt.py <dir> --kind <kind> --label <label> --mem <GB> [--route R] [--result RES] [--node N] [--extra "..."]`
   This builds `prompts_out/<label>.md` from `prompts/<kind>.md` plus the current state: target, route/node cards,
   barrier list, pool notes for the route's inputs, memory cap, return conditions. It stamps a state hash.
2. `PY -I RC/check_launch.py <dir> --kind <gate kind> --label <label> --mem <GB> --prompt <file> [--route R] [--result RES]`
   (make_prompt prints this exact command).
   - **PASS** registers the run in `ledger.md`.
   - **REJECT** lists the reasons. Fix them, or queue the launch until a slot frees. Never work around a REJECT:
     if the budget is the obstacle and waiting is not acceptable, ask the user to raise it.
3. Launch the Agent with `description` = the label and a SHORT prompt: "Read your full instructions in <file> and
   follow them exactly." Keep it in the background. The long prompt never enters your context.
4. When it returns, read only its SUMMARY block; open its run file only when you need a detail. Then:
   - run `finish_run.py <dir> <Lid> --outcome "..." --tokens N --minutes M --knowable yes|no|partly`, taking the
     tokens and minutes from the task notification;
   - update the cards (route verdict/status, barriers, results, tree);
   - run `merge_pool.py <dir>` if the agent wrote a pool shard;
   - run `tree_status.py <dir>`.

**When the target or a route card changes while agents are running**, regenerate their prompts. Send a running
agent a SendMessage only when the change invalidates its work, and then say what changed and where to read it.
Mid-run retargeting was a big waste last time; phases 2 and 5 exist to avoid it.

**After a session restart**, background agents from the old session are gone:
1. Run `status.py`.
2. For each `running` ledger entry, check whether the agent still exists. If it does not, close the entry with
   `finish_run.py ... --outcome "lost on restart"`.
3. Relaunch through the protocol. The run file holds the agent's progress, so point the new agent at it in
   `--extra`.

## Standing rules, and why they exist

1. **The budget belongs to the user.** budget.toml, overridden by budget.local.toml and an optional per-campaign
   budget.toml, sets the maximum
   number of concurrent agents, the total memory and the memory per agent. Never edit it and never exceed it;
   check_launch re-reads it on every launch. Each prompt carries that agent's memory cap. In the campaign
   behind this skill, uncapped parallel JVMs filled the machine's RAM.
2. **No launch without a PASS.** The gate checks:
   - budget;
   - target status;
   - complete route cards;
   - dedup against siblings with the same method class (and against killed ones unless `bypasses` names the
     barrier). A different deliverable is a real difference: merge only when the WHOLE deliverable coincides,
     never just because two launches read the same sources. A partial overlap is a TRIM, not a merge: launch it
     with the overlapping part cut out and pointed at the other run's output;
   - the per-node active limit;
   - one check per result;
   - prompt markers, and a fresh state hash.
3. **The target comes before any attack.** Scouts and attacks need `target_status: confirmed`, which only the
   user's OK in phase 5 gives. The tool hunt needs `cross-checked`.
4. **Ceiling before effort.** No attack without a written ideal ceiling that meets the need. A KILL needs a
   derivation of at most 5 lines that anyone can re-check. When unsure, mark UNCERTAIN and send a scout. Never
   kill on a hunch: false kills are the expensive error. A KILL resting on a published theorem is final: record
   it before any computation, and run nothing to "confirm" it.
5. **One independent check per result version.** Main-thread checks count. Launch it when the result is
   registered, also for results off the main line. Never stack checks, and do not "just double-check" a passed
   result. A changed result is `bump`ed and gets its one new check. The final audit (phase
   12) is not a repeat: it checks that the pieces compose, which no single check covered.
6. **Claim hygiene.** Before relaying a number or a literature claim to the user, or writing it into another
   agent's target, spend two minutes on the primary source. This is where last campaign's real errors were.
7. **Others' results are inputs.** Use published, posted or AI-assisted results of other people as given: verify
   that the citation is accurate and that their hypotheses match ours, but do not audit their proofs. This
   includes released constructions and code: an attack on a construction record starts from the released record.
8. **There are no time caps.** The user rejected time budgets. Agents stop on bounded deliverables and on
   content-based return conditions instead (scout: ceiling + verdict; attack: the five conditions).
9. **Say "what's still missing", not "impossible".** Treat barriers as the next target: each new barrier triggers
   a mode-B tool hunt. Declare a route class dead only after a real attempt or a written ceiling.
10. **Nothing outward-facing without the user.** That covers posting, submitting, registering, and emailing
    authors. Prepare the materials, and let the user decide.

## User touchpoints

Only these interrupt the user; otherwise keep the campaign moving:
- kickoff confirmation (0);
- a scoop or a moved record (1, 12);
- target card + tree (5);
- conjecture-strength routes (7);
- a stop-rule report (10);
- a budget raise request (any time);
- an audit failure that forces major rework (12);
- delivery (14).

## Evaluation data for the skill itself

The ledger records tokens, minutes and `knowable_in_advance` for every run. At delivery, or when the campaign
stops, summarise:
- tokens by kind;
- the number of kills at the ceiling gate and what they saved;
- runs whose outcome was knowable in advance;
- false kills, if any surfaced.

Append the summary to the end of the campaign's `ledger.md` and include it in the delivery message. It is the
data for evaluating this skill.

## Script reference

| script | purpose |
|---|---|
| `init_campaign.py` | new campaign / `--dir` resume (prints status) / `--inherit-from` |
| `status.py <dir>` | stage, target, budget use, running agents, routes, results, tree root, stop signals |
| `make_prompt.py` | build a prompt file for a kind: lit_sweep, lit_verify, lit_read, quant, tool, scout, attack, referee, audit_logic, audit_numerics, audit_lit, paper, lean |
| `check_launch.py` | the gate. Gate kinds: lit, read, quant, tool, scout, attack, referee, audit, paper, lean, other |
| `finish_run.py` | close a ledger entry; optionally set the route status, outcome or blocked_by, or the result's check status |
| `result.py` | `add` / `check` (main-thread check) / `bump` / `freeze` for the results registry |
| `merge_pool.py <dir>` | merge pool shards into lit_pool.md; report rough entries, duplicates, obstructions, unread entries |
| `tree_status.py <dir>` | the AND/OR tree with propagated states, plus the STOP RULE and barrier-convergence signals |
| `tests/selftest.py` | end-to-end test of every gate on a throwaway campaign; run it after changing any script |
