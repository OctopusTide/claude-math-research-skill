# Attack route {{ROUTE_ID}}, agent {{LABEL}}

{{TARGET_BLOCK}}

## The route card (it passed the ceiling gate)

{{ROUTE_CARD}}

## The tree node it serves

{{NODE_CARD}}

{{BARRIERS_BLOCK}}

## Pool notes for this route (use these instead of re-reading the sources)

{{POOL_NOTES}}

Extra instructions: {{EXTRA}}

## Your task

Carry out this route: prove, construct or compute what the node needs, at the needed value in the unified
unit. The done-criterion is on the node card.

RETURN WHEN: any one of these holds. Return at once; do not push on past it.
1. **Target reached.** You have the result at the needed value. State it exactly: hypotheses, constants, range.
2. **Named barrier.** You hit an obstruction you can name. Give its statement, scope and evidence. If it is
   already in KNOWN BARRIERS, give its ID.
3. **Ceiling wrong.** The route card's ceiling turns out wrong; for example, the achievable value is below the
   ideal one. Give the corrected value and why.
4. **Sub-lemma needed.** You need a new sub-lemma that is a project in itself. Return a proposed split: its
   statement, the numeric target it needs, and why you need it. Do not dive in.
5. **Three failures.** Three genuinely different approaches have failed on the same sub-step. List them and say
   what each one lacked.

A partial gain counts too. Report it in the unified unit, so it can be placed on the ladder.

{{COMMON_RULES}}

## SUMMARY (your final message)
- route: {{ROUTE_ID}}; return condition: <1-5>
- result: <exact statement, or "none">; value: <...> <unit> vs needed <...>
- proposed check for this result: <what ONE independent check would confirm it: referee scope / independent code>
- new barrier: <statement; scope; evidence, or "none">
- split proposal: <sub-lemma + its target, or "none">
- new pool entries: <IDs>
- details: {{RUN_FILE}} §<sections>
