# Barrier registry

Named obstructions with scope and evidence. Every agent prompt lists them (KNOWN BARRIERS), so nobody re-derives
them. Every new barrier triggers one targeted search: "how have others got around this?" (phase 4, mode B).

```
Card format (example; fenced blocks are ignored):

## B03 Square-root barrier for family averaging
- statement: averaging over the family saves at most sqrt(|F|), which needs |F| >= q^2; only |F| ~ q is available
- scope: method classes family-averaging, expansion; nodes N2
- evidence: runs/R05.md §3; Paper Y, §6 remark (P-R2-004)
- found_by: R05 (L014)
- date: 2026-01-15
- workaround_search: pending          (pending | done -> pool IDs found)
```
