# Problem tree (AND/OR)

Built in phase 3 from the cross-checked TARGET card. Tool hunt (phase 4) adds OR branches. Route cards attach to
nodes via their `node:` field, so every OR child that is a concrete method is a route card, not a node.
Run tree_status.py to see states propagated up from the routes.

```
Card format (example; fenced blocks are ignored by the scripts):

## N0 Constant c <= 1.200
- type: AND                  (AND: all children needed | OR: any child suffices)
- parent: -
- statement: delta >= 0.031 in the unified unit
- needed: delta >= 0.031

## N2 Error-term estimate in the short range
- type: OR
- parent: N0
- statement: bound the short-range error term with exponent <= 0.30
- needed: exponent <= 0.30
- gap_share: closes 100% of the gap alone (from TARGET.sensitivity)
- done_when: proof of the edge estimate passes its one check
- inputs: P-V2-003, P-R1-001
- status_override:           (optional: solved | blocked | open, with a note why)
```

Leaf test: a leaf node is small enough when one agent could take it and know exactly what to hand back:
a one-line statement, a numeric target, a done-criterion, its inputs, and its share of the gap. If a leaf is
really "invent a new method", split it further or mark it open-problem strength and tell the user.

## N0 {{root: the user's goal}}
- type: AND
- parent: -
- statement:
- needed:
