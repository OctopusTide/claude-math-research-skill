# Route cards (6), ceiling gate (7), attack (8), checks (9), loop and stop (10)

## Phase 6: route cards

Write one card per concrete method on an OR node, in `routes.md`, in the main thread. The format is in the
template. Fill in everything except the ceiling fields: they are bookkeeping, a minute or two each.

- **`method_class`.** Use a short, stable tag (moment-method, sum-of-squares, lattice-reduction, sat-encoding, ...).
  Reuse existing tags: the dedup check compares normalised tags on the same node.
- **`needed` / `needed_value` / `better`.** These come from the node, which came from the TARGET sensitivity table.
- **`inputs`.** The pool IDs of every theorem the route borrows. `make_prompt.py` pastes those entries' notes into
  scout and attack prompts, so agents don't re-read papers.
- **`differs_from`.** Required when a sibling on the same node has the same method class. If you cannot write a
  real difference, merge the two routes instead. A different DELIVERABLE is a real difference: two routes that
  read the same papers but hand back different things (notes vs. a calibrated computation, a bound vs. a
  construction) are not duplicates. Merge only when the WHOLE deliverable coincides. When a launch overlaps
  another only in part (some of the same reading, a different end product), TRIM it: launch it with the
  overlapping part removed and pointed at the other run's output. Merging a partial overlap throws away the part
  that was new.

## Phase 7: the ceiling gate

**Why.** In the campaign this skill was built from, about a quarter of the attack runs (~1.5M tokens) were decided
by something a one-line or ten-minute check would have shown:
- an ideal ceiling below the need;
- a gain that was positive but far too small to matter;
- an obstruction stated explicitly in a paper already in hand;
- a borrowed theorem whose hypotheses did not match the setting.

The ideal ceiling is the best the method class could do under the most favourable assumptions: perfect
cancellation, the conjectured exponent, optimal free parameters.

Fill the ceiling in one of three ways:

| case | who | how |
|---|---|---|
| one-line computation, or a barrier / pool note settles it | coordinator, in the main thread | fill `ceiling`, `ceiling_value`, `derivation`, `verdict` directly |
| needs reading a theorem's hypotheses, or a non-trivial derivation | scout agent (`--kind scout`) | the agent hands back a ceiling, a hypothesis check and a verdict, then stops |
| needs numerics | scout agent, using the campaign's calibrated model, memory from the budget | same |

- One scout may carry several cards that need the same literature (list them in `--extra`). Launch it on one of
  the routes and note the others.
- Scouts launch with the verdict `pending` or `UNCERTAIN`.

Verdicts:
- **GO:** the ceiling meets `needed_value` with margin (`check_launch.py` verifies the numbers for `better`
  higher/lower).
- **KILL:** the ceiling misses, OR a registered barrier applies, OR a borrowed theorem's hypothesis fails.
  - Set `status: killed` and `blocked_by: <barrier>`. Create a barrier card if this is a new obstruction.
  - That triggers a mode-B tool hunt ("how did others get around it?").
  - **A KILL that rests on a published theorem is final** (a proven upper bound, an exact value, a stated
    impossibility). Record it as soon as the theorem is in hand, before any computation, and do not run solvers
    or searches to "confirm" it: the theorem is the evidence (standing rule 7). In the skill's test runs, a
    7-minute solver run after such a KILL produced nothing.
- **CONJ:** reaching the target needs more than about half the gap to a famous conjecture. Ask the user. Only
  `user_approved: yes` lets it attack.
- **UNCERTAIN:** the ceiling hinges on a judgement you cannot settle. Send a scout; do not kill on a hunch.

**False kills are the costly error.** That is why the derivation is written out, at most 5 lines. If anyone later
finds it wrong, reopen the route (`status: draft`, verdict `pending`) and note why on the card.

## Phase 8: attack

Order the GO routes as follows:
1. Routes under the bottleneck AND-child come first.
2. Within one OR node, the highest ceiling margin and the lowest cost come first.
3. At most `max_active_per_or_node` (budget.toml, default 2) may be active on one node at a time.

When the budget is full, routes wait as `status: queued`.

Launch with the standard protocol: make_prompt → check_launch → Agent. The attack template carries the five return
conditions:
1. target reached;
2. named barrier;
3. ceiling wrong;
4. needs a new sub-lemma (returns a proposed split);
5. three different approaches failed on the same sub-step.

There is no time limit: the user rejected time budgets. Bounded deliverables replace them.

**Construction and optimisation targets start from the released record.** If the pool entry of the current record
has `artifacts:` (a construction, certificate, code or data), the attack route starts from it: download it into
the run folder, reproduce the record value first, then improve. A local improvement of a released record is a
valid result; say plainly that it is one. Put the link in the route card's `inputs` so make_prompt passes it on.

On return, read only the SUMMARY, then act on its return condition:

| return | coordinator action |
|---|---|
| 1 reached | `result.py add`, with a check plan taken from the agent's "proposed check"; the route becomes `status: done`, `outcome: positive` once the check passes |
| partial gain | record the value on the route card. Place it on the ladder, and say which rung it reaches. Gains too small for any rung are marked "no use" |
| 2 barrier | create or extend the barrier card; route `status: blocked`, `blocked_by`; launch a mode-B tool hunt |
| 3 ceiling wrong | fix the card's ceiling and derivation, and re-run the gate (verdict may flip to KILL) |
| 4 split | add the sub-lemma as a new tree node with its own target; write a route card for it |
| 5 three failures | `status: blocked`, with the three approaches noted; consider a barrier card if they share a cause |

Always run `finish_run.py <dir> <Lid> --outcome ... --tokens N --minutes M --knowable yes|no|partly`. Take the
tokens and minutes from the task notification. `--knowable` says whether this outcome could have been known
before launch; answer it honestly. It is the skill's own evaluation data.

## Phase 9: one check per result

**Why.** Measured on the last campaign, 8 referee runs (~2.2M tokens) found zero fatal errors. The two real errors
were relayed claims that were never checked (a misquoted saving exponent and a misquoted constant). Meanwhile one
result was checked four or five times. The rule: every positive result gets exactly ONE independent check, chosen
when it is registered.

- **Launch the check when the result is registered.** Being off the main line is not a reason to defer or skip
  it: an off-path result still gets its one check, just never more than one.
- `result.py add ... --check-plan "<who/what>"`. The plan names either:
  - a referee agent with a narrow scope: the NEW step, plus independent code for numerics; or
  - a main-thread check you will do yourself.
- **Referee:** `make_prompt.py --kind referee --result RES-xx --extra "<scope>"`, then
  `check_launch.py --kind referee --result RES-xx`. The registry refuses a second check on the same version.
- **Main-thread check:** `result.py check RES-xx --by "..." --status passed|failed`. Refused if the version
  already has its check.
- **The check fails, or the result changes:** `result.py bump RES-xx --why ...` reopens the slot. It lists
  dependents, whose results must be re-examined.
- **Referees do not block.** Downstream work may use a "pending" result. If it then fails, the dependents listed by
  `bump` are rolled back.

**Claim hygiene (separate from the one check).** Before you relay any number or literature claim to the user, or
write it into another agent's prompt as a target, spend two minutes on the primary source: the agent's run file,
the code output, or the pool entry's source. A value that already passed its one check needs no second look.

## Phase 10: loop and stop

After every return:
1. update the cards;
2. `merge_pool.py` if shards changed;
3. `tree_status.py`.

- **The root is solved:** go to phase 11.
- **STOP RULE: the root is blocked**, or `tree_status.py` prints a STOP-RULE SIGNAL (one barrier blocking 3
  independent method classes). Stop launching on that path and tell the user, in their language:
  - what is still missing, naming the exact blocked leaves and their barriers;
  - what strength is needed, e.g. "short-sum cancellation close to the strength of the exponent-pair conjecture";
  - which rung of the ladder the campaign did reach;
  - options: continue with conjecture-strength routes; retarget to a lower rung; pause.
- **Otherwise:** launch the next queued routes and any mode-B tool hunts. Ask the user only at the user
  touchpoints.
