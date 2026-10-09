# Target quantification (phase 2), problem tree (phase 3), user review (phase 5)

## Phase 2: one normalised target number, computed twice, blind

**Why.** Every later decision compares something against this number: route ceilings, partial gains, the stop rule.
In the campaign this skill was built from, the decisive target number arrived only after the attack agents had
launched, so their
prompts had to be re-sent. A wrong target silently corrupts everything downstream. That is why the user asked for
two independent quantifiers and a careful cross-check.

### Launch

Run two agents in parallel, each with `make_prompt.py --kind quant`:
- **Q1:** `--extra "Method: derive from the papers' formulas (pool notes P-...)"`.
- **Q2:** `--extra "Method: reproduce from the public code/data (paths ...)"`, or "write your own model in a
  different language", or another genuinely different method.

Different methods are the point: two agents using the same method share the same blind spots. Neither may see the
other's files, and the prompt says so. Memory: give the numeric one most of the budget.

### Cross-check (coordinator, after both return)

1. **Calibration first.** Each must reproduce a known record with the record holder's inputs. A run that cannot is
   discarded, whatever its target says.
2. **Compare link by link** along the translation chain, not just the final number. A matching final number with
   different intermediate values usually means compensating errors.
3. **Compare the sensitivity tables:** same bottleneck component? Same order of magnitude for each component's
   needed improvement? The tables must be in the record method's own parameters (which part of the record
   construction or proof must improve, and by how much), not only in the goal's unit. Send back a table that
   only says "need value V".
4. **When they agree,** that agreement IS the one independent verification. Do not add more rounds.
5. **When they disagree,** find the FIRST link where they differ.
   - Settle that one link yourself: open the primary source, or recompute just that step.
   - Only if you cannot, launch a third agent scoped to that single link (`--kind quant --label Q3`, with
     `--extra` stating the disputed link and both values).
6. Fill the TARGET card:
   - statement, value, unit, better, record_value;
   - chain;
   - model (path + the record it reproduces);
   - sensitivity;
   - ladder;
   - quant_runs;
   - crosscheck: per link "agree" or "disagree -> resolved how".
7. Set `target_status: cross-checked`. Only the user's OK in phase 5 makes it `confirmed`. The scripts refuse
   scouts and attacks before that.

For construction problems the chain is often one line. For example: "beat 1.551 at size n" means "find an object
of size >= 1.552^n". Still run both quantifiers; they will be fast.

## Phase 3: the AND/OR problem tree

**Why.** It turns the gap into small problems with clear targets. It also makes three things mechanical:
- **Duplicate detection.** Two routes on the same node with the same method class get flagged.
- **Prioritisation.** The bottleneck AND-child goes first.
- **The stop rule.** Blocked states propagate to the root.

Build it in the main thread (it needs the global view), in `tree.md`:
- **Root N0** is the TARGET.
- **AND nodes** are conditions that must all hold, e.g. a short-range estimate AND a long-range estimate.
  Their `needed:` values come from the sensitivity table.
- **OR nodes** are alternative ways to meet one condition. Their concrete methods become ROUTE CARDS attached by
  `node:`, not further nodes.
- **Leaves** must pass the leaf test:
  - a one-line statement;
  - a numeric target;
  - a done-criterion;
  - inputs (pool IDs);
  - a gap share.

  A leaf that is really "invent a new method" is not small enough. Split it, or mark it open-problem strength.
- Also put partial-credit milestones from the ladder on the nodes (e.g. "enough for the intermediate milestone, not for the goal"). A partial
  result can then be placed.

Draft the OR branches widely, from the pool: the cross-field and tool entries especially. Phase 4 (tool hunt) will
add more. Run `tree_status.py` to see the structure.

## Phase 5: report to the user (one message, then wait)

Run this after the tool hunt, so the tree shown is complete. Send ONE message, in the user's language:

- **Target card:** chain, target value and unit, current record in the same unit, bottleneck, ladder. Add one
  line on the cross-check: "the two independent quantifications agree" or "they disagreed at link k; resolved
  by ...".
- **Problem tree:** `tree_status.py` output, trimmed to the important nodes, with each OR node's candidate routes.
- **Literature:** any record changes or near-scoops.
- **Decisions for you:** e.g. whether to accept a conjecture-strength node; which ladder rung counts as success.

Only after the user's OK: set `target_status: confirmed`, log it under User decisions, and set
`stage: 6-routes`.
