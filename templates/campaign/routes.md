# Route cards

One card per concrete method attached to a tree node (phase 6). The coordinator writes everything except the
ceiling fields; the ceiling gate (phase 7) fills those, by a one-line computation or barrier lookup, or by a scout.
check_launch.py reads these cards, so keep the field names.

```
Card format (example; fenced blocks are ignored):

## R07 Weighted moment method for the error term
- method_class: moment-method         (short controlled tag; same tag + same node = duplicate)
- node: N2                            (tree node it attacks)
- mechanism: bound the error term by a 4th moment with optimised weights
- needed: error exponent <= 0.30 (from TARGET via sensitivity)
- needed_value: 0.30
- better: lower                       (higher | lower | n/a)
- inputs: P-L0-012, P-V1-004          (pool entries with the theorems used, incl. exact hypotheses)
- differs_from:                       (required if a sibling with the same method_class exists: name it + the real difference)
- bypasses:                           (required to relaunch a killed method class: the barrier ID it gets around)
- ceiling: 0.34 even with optimal weights and the conjectured moment bound
- ceiling_value: 0.34
- derivation: <= 5 lines anyone can re-check
- hypotheses_check: Theorem X needs prime moduli; ours are composite -> mismatch   (when an external theorem is used)
- barriers_checked: B2 not applicable because ...
- verdict: KILL                       (pending | GO | KILL | CONJ | UNCERTAIN)
- user_approved:                      (yes, only for CONJ routes the user chose to pursue)
- memory_gb: 0
- status: killed                      (draft | queued | scouting | attacking | done | blocked | killed | shelved)
- outcome:                            (positive | negative | partial — set when done)
- blocked_by:                         (barrier IDs, when blocked or killed)
- agent:                              (set by check_launch.py)
```
