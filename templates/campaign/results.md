# Results registry

Every positive result we produce gets an ID, a version, and exactly ONE designated independent check, chosen
when it is registered (result.py add --check-plan ...). A check done by the coordinator in the main thread
counts as that check (result.py check ...). check_launch.py refuses a second referee on the same version;
only a changed result (result.py bump) reopens the slot. Others' published results are not registered here:
they live in the pool and are used as given.

```
Card format (example; fenced blocks are ignored):

## RES-01 Improved bilinear estimate in the long range
- route: R03
- version: 2
- statement: for 6a + 2b < 1 ... (exact statement)
- value: range edge 0.54 (unified unit)
- depends_on: P-L0-007, RES-00
- check_plan: referee agent, independent derivation of step 4
- check_status: passed               (none | pending | passed | failed)
- check_by: referee REF-R03
- check_ref: L019
- frozen: no                         (phase 11 sets "yes (vN, date)")
- history: v1 -> v2: constant fixed after referee
```
