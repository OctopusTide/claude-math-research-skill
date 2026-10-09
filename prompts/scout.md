# Ceiling scout for route {{ROUTE_ID}}, agent {{LABEL}}

{{TARGET_BLOCK}}

## The route card

{{ROUTE_CARD}}

## Its tree node

{{NODE_CARD}}

{{BARRIERS_BLOCK}}

## Pool notes for this route

{{POOL_NOTES}}

Extra instructions: {{EXTRA}}

## Your task: fill the ceiling, then stop

You are NOT attacking the route. You only decide whether attacking it can possibly pay off. Hand back three
things.

1. **Ideal ceiling.** Give the best value this method class could reach under the most favourable assumptions:
   perfect cancellation, the conjectured best exponent, an optimal choice of every free parameter. Put it in the
   unified unit, with a derivation of at most 5 lines that anyone can re-check. If you need numerics, use the
   campaign's calibrated model (see the TARGET card's `model:`).
2. **Hypothesis check.** For every external theorem the route relies on, check its exact hypotheses against our
   setting: match / mismatch (which one) / unclear.
3. **Verdict.** Choose one of:
   - **GO**: the ceiling meets the needed value with margin;
   - **KILL**: the ceiling misses, OR a registered barrier applies, OR a hypothesis fails;
   - **CONJ**: reaching the target needs more than half the gap to a famous conjecture. Name the conjecture and
     the fraction;
   - **UNCERTAIN**: say exactly which judgement you could not settle.

RETURN WHEN: the three items are written. Do not continue into the proof, even if it looks promising. Write
"promising: <one line>" instead.

{{COMMON_RULES}}

## SUMMARY (your final message)
- route: {{ROUTE_ID}}
- ceiling: <value> <unit> vs needed <value>; derivation in <run file section>
- hypotheses: <theorem: match/mismatch(which)/unclear; ...>
- barriers: <applicable IDs or "none">; new obstruction found: <statement + evidence, or "none">
- verdict: GO | KILL | CONJ (<conjecture>, <fraction of gap>) | UNCERTAIN (<what>)
