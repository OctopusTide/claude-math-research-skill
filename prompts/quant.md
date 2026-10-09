# Target quantification (independent, blind), agent {{LABEL}}

Goal of the campaign, in the user's words: {{GOAL}}

Another agent is doing this same task independently. You will not see its work, and it will not see yours. The
coordinator compares the two link by link, so work it out yourself and do not look for its files.

{{EXTRA}}

## Your task

Turn the goal into ONE normalised target number that every attack route can be measured against.

1. **Translation chain.** Write the chain from the user's goal to a technical quantity, one link per step, e.g.
   "c <= 1.20 -> inequality Z at k = 12 -> error exponent -> delta >= 0.031". For each link, cite the pool entry or
   the computation behind it.
2. **Model.** Build or reuse a numeric model that maps the inputs to the goal. Before you trust it, it MUST
   reproduce at least one known record, using the record holder's inputs (from the pool notes). If it cannot,
   report that: an uncalibrated model gives a worthless target. If the chain is exact arithmetic (common for
   construction problems: "size N in dimension n beats the record"), there is no model to calibrate; say so.
   Re-building the record's construction itself is attack work, not quantification.
3. **Target.** State the target in one unit (statement, value, unit, better = higher|lower), and convert the
   current record into the same unit.
4. **Sensitivity table, in the record method's own parameters.** Read the record-setting construction or proof
   first (pool notes; read it yourself if the notes lack its parameters). For each of its components or
   parameters, give how much it must improve, ON ITS OWN, to reach the target, e.g. "one more element of type X
   in the base object" or "exponent a -> a - 0.002". A table only in the goal's own unit ("need size 368") is not
   enough: attacks need to know which part of the record to improve. Mark the bottleneck.
5. **Ladder.** Give the value needed for each meaningful milestone between the current record and the goal.

Use the method named in the extra instructions above if one is given (the two quantifiers are deliberately sent
down different methods). Otherwise choose your own and say which.

RETURN WHEN: all five items are done, and the model reproduces a known record (or you have shown precisely why it
cannot).

{{COMMON_RULES}}

## SUMMARY (your final message)
- chain: <link -> link -> ... with the value at each link>
- calibration: reproduces <record> as <value> (code: <path>)
- TARGET: <statement> = <value> <unit>, better = <higher|lower>; record in same unit: <value>
- sensitivity: <component: needed alone; ...>; bottleneck: <component>
- ladder: <milestone: value; ...>
- doubts: <the links you are least sure of>
