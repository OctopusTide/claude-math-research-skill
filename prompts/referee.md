# Independent check of {{RESULT_ID}}, agent {{LABEL}}

RESULT UNDER CHECK:
{{RESULT_CARD}}

{{TARGET_BLOCK}}

Pool notes for the inputs it uses (others' results; use them as given, but check their hypotheses are met):
{{POOL_NOTES}}

## Scope

{{EXTRA}}

## Your task

You are the ONE independent check this result version gets. Nobody re-checks it after you, so be careful, and
keep to the scope.

- **Proofs.** Concentrate on the NEW step, the one that carries the gain. Re-derive it yourself, preferably by a
  route different from the author's. Check that every borrowed theorem's hypotheses are met. Skip the standard
  parts unless they are modified.
- **Numerics.** Write INDEPENDENT code. Do not run or edit the author's code; read it only to learn the
  conventions. Reproduce the claimed numbers, with rigorous rounding (exact rationals or interval arithmetic)
  wherever the claim is a rigorous bound.
- Classify every issue as:
  - FATAL: the result is false, or does not follow;
  - FIXABLE: it is true after a stated correction, and you say whether any constant changes;
  - MINOR: wording or documentation.

RETURN WHEN: you have reached a verdict.

{{COMMON_RULES}}

## SUMMARY (your final message)
- result: {{RESULT_ID}}
- verdict: VALID | VALID WITH FIXES | INVALID
- fatal: <list or "none">; fixable: <list, with constant changes>; minor: <count>
- independent reproduction: <what you recomputed and the values you got>
- corrected statement (if fixes change it): <...>
