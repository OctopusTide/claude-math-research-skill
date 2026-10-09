# research-campaign

A Claude Code skill for doing math research with a team of subagents: beating a record, pushing an explicit
bound, improving a constant, attacking a chain of lemmas, or certifying a computation.

It grew out of a long multi-agent campaign. Looking back, most of the wasted tokens could have been spotted
before anything was launched:

- attacks whose best possible outcome still fell short of the target;
- obstructions already written down in a paper we cited;
- borrowed theorems whose hypotheses didn't fit;
- two agents doing the same job;
- a record that had already been beaten, posted on someone's faculty page;
- results checked four times while the real errors sat in claims nobody checked.

The skill puts a cheap check in front of each of these.

## How it works

1. **Kickoff.** You set the budget: how many agents, how much memory.
2. **Literature pool.** One agent sweeps wide, others verify by source type, then the important papers get a close
   read. The search covers the target number itself, personal pages, the full text of recent AI and
   computational-discovery papers, and any released constructions or code.
3. **Target.** Two agents work out independently what exactly has to improve, and their answers are checked
   against each other step by step.
4. **Problem tree.** The goal is split into an AND/OR tree of small subproblems, each with a numeric target. For
   each bottleneck, an agent looks for tools other people have found.
5. **Route cards.** Every route gets its best-case ceiling worked out before anyone attacks it. If the ceiling
   misses the target, the route is dropped.
6. **Launch check.** `check_launch.py` looks at the budget, the target, duplicates, earlier kills and stale prompts.
7. **Attacks** come back when they reach the target, hit a named barrier, find the ceiling was wrong, need a new
   lemma, or fail three different ways. There are no time limits.
8. **One independent check per result.** A second check of the same version is refused.
9. **Stop rule.** If the root is blocked, or one barrier has stopped three different methods, the campaign stops
   and tells you why.
10. **Closing.** Freeze the results, run one audit of the whole chain, then write the paper and the Lean
    formalisation in parallel.

## Install

Copy this folder to `~/.claude/skills/research-campaign/` to use it everywhere, or to `<project>/.claude/skills/`
for a single project. You need Claude Code with subagents, web search and a shell, plus Python 3.11+ (standard
library only). Lean 4 + Mathlib and a TeX engine are optional.

## Configure

Put your own settings next to `SKILL.md`:

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

A campaign can override the budget with its own `budget.toml`.

## Use

Just ask: "start a campaign to beat the record for X", "resume the campaign", "push this bound below 1.2". The
skill sets up `campaigns/<date>-<slug>/` in your project with the card files the scripts read and update
(`CAMPAIGN.md`, `tree.md`, `routes.md`, `barriers.md`, `results.md`, `ledger.md`, `lit_pool/`). Small one-agent
tasks of under half an hour get a light mode without all that.

After changing a script, run `python -I tests/selftest.py`.

## Results

On long campaigns it saves about 20% of subagent tokens. We replayed a 3.7-hour window of a real campaign blind
(30 launches, 9.7M tokens). The gate stopped 7 launches, all of them rightly, for an 18.5% net saving after
paying for itself.

We also wrote 203 test cases, each a campaign snapshot with one planted mistake (17 kinds of mistake, 12 areas of
math). With Sonnet 5.5 as the gate it got 97% right, and it never stopped a good launch or waved a bad one
through.

Both tests are small and in-house, so read the numbers as a ballpark.

## Problems we found

1. **A wrong merge.** The gate merged two launches that shared some reading but produced different things. It now
   compares what each run delivers, and a partial overlap gets trimmed instead of merged.
2. **Results buried in a paper's body.** A record that appeared only inside a machine-learning paper, with nothing
   in the abstract, was missed every time. We added a sweep through the full text of methods papers, but agents
   still skip it. This one is still open.
3. **No savings on small tasks.** On ~30-minute tasks the skill cost 18–37% more tokens, mostly from reading it.
   Those tasks now get a light mode.
4. **Running a solver on a settled question.** One agent spent 7 minutes confirming something a published theorem
   had already ruled out. A kill backed by a theorem is now final.
5. **Targets too coarse.** Target work stopped at "we need size 368" instead of saying which part of the record
   construction has to get better. The quantification prompt now asks for that.
6. **Moved records.** When the record turned out to have moved, one agent stopped and another kept going. Now it
   reports the new record and retargets, as long as the new target still clears the ceiling check.
7. **Starting from scratch.** Runs that knew the record construction rebuilt it from zero. They now start from the
   released construction or code.
8. **Late checks.** Results off the main line had their check put off. Every result now gets its check when it is
   registered.
9. **Weaker models as the gate.** Haiku follows clear rules fine, but it is noisy on real transcripts and shallow
   at literature search. Use a stronger model for those two jobs.
10. **Waiting instead of scouting.** Most misses on the test cases chose "wait" where the right call was a quick
    ceiling scout or a trimmed launch.
11. **The stop rule gets lost in the prose.** When one barrier had already blocked three methods, the gate always
    killed the fourth route but mentioned the campaign stop rule only 5 times out of 12. `status.py` and
    `tree_status.py` flag it regardless.

## Files

- `SKILL.md`: the pipeline, the standing rules and when to ask the user.
- `references/`: one file per group of phases (literature, target and tree, routes and attack, closing).
- `prompts/`: templates for each kind of subagent, filled in by `scripts/make_prompt.py`.
- `scripts/`: `init_campaign`, `status`, `make_prompt`, `check_launch`, `finish_run`, `result`, `merge_pool`,
  `tree_status`, `rclib`.
- `templates/campaign/`: the card files a new campaign starts from.
- `tests/selftest.py`: an end-to-end test of every gate on a throwaway campaign.
- `config.toml`, `budget.toml`: shipped defaults.

## License

MIT
