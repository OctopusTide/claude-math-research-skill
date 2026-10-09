# Claude Math Research Skill

[中文说明](README.zh-CN.md)

A Claude Code skill (`research-campaign`) for doing math research with many sub-agents: pushing bounds and
records, searching the literature, checking proofs, and formalizing in Lean.

## Where it comes from

We used Claude with many sub-agents on a long math research project: improving a known bound. Looking back, a
lot of tokens went to things we could have avoided from the start:

1. **Attempts that could never reach the target.** Even in the best case, some approaches could not get the
   number we needed. A few lines of arithmetic would have shown it.
2. **Running into known obstacles.** Some of them were already written in papers we had cited.
3. **Theorems that didn't apply.** Agents borrowed theorems whose conditions don't hold in our setting.
4. **Duplicate work.** Two agents doing the same job.
5. **Missing the latest record.** The record had already been improved; the new result was on a professor's
   personal page.
6. **Checking the wrong things.** Some results were checked four times, while the real errors sat in results
   nobody checked.

## What the skill does

Before spending tokens, it runs a cheap check for each of these:

1. Before an attempt, work out the best it could possibly reach. If that misses the target, don't launch it.
2. Keep a list of known obstacles, and stop new attempts that run into one.
3. Before using someone's theorem, check its conditions against our setting.
4. Compare each new task with running and finished ones. The same job is merged; partial overlap is cut out.
5. Search the literature first, including personal pages, the exact target number, and released code.
6. Check every result exactly once, independently.

It also keeps to a budget you set (agents, memory), breaks the goal into small subproblems, and stops when every
path is blocked. At the end it can write a paper and a Lean formalization.

## Results

On long projects it saves about 20% of tokens. We replayed 3.7 hours of a real project: the checks would have
stopped 7 of 30 launches, all of them rightly.

## Problems we found in testing, and the fixes

| Problem | Fix |
|---|---|
| Two tasks that only partly overlapped were merged | Compare what each delivers; cut only the overlapping part |
| A solver was run to confirm what a published theorem had already settled | A stop backed by a theorem is final |
| Agents ignored a record's released construction and started from zero | Start from the released construction or code |
| The record moved mid-run, and agents reacted differently | Report it, then go for the new record if it is still reachable |
| Targets were too vague ("need size 368") | Say which part of the record method has to improve |
| Some results never got checked | Every result is checked when it is registered |
| On ~30-minute tasks it cost more than it saved | Short tasks use a light mode |
| A record hidden in the body of a machine-learning paper was never found | Not solved yet |
| Haiku was too unreliable as the checker | Use Sonnet or a stronger model |

## Install and use

```bash
git clone https://github.com/OctopusTide/claude-math-research-skill ~/.claude/skills/research-campaign
```

Or clone it into `.claude/skills/research-campaign` inside one project. You need Python 3.11+. Lean and LaTeX are
optional.

Then ask Claude, for example: "start a campaign to beat the record for X", or "continue the campaign".

To change settings, copy `config.toml` or `budget.toml` to `config.local.toml` or `budget.local.toml` and edit it.
The comments in those files explain each setting.

## License

MIT
