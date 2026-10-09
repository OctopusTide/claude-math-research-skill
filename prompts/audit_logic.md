# Final audit — logical chain, agent {{LABEL}}

{{TARGET_BLOCK}}

You are a fresh reader. You did not take part in the campaign. Work ONLY from the frozen package in
{{PACKAGE_DIR}}:
- MAIN.md: main theorem and dependency graph;
- results/: our results, each at its frozen version, with its one check;
- cited.md: others' results we use, with pool IDs.

Extra instructions: {{EXTRA}}

## Your task

The pieces were each checked once. Your job is to check that they COMPOSE, i.e. that the assembled chain proves
the main theorem. Go through it link by link.

- **Hypotheses.** Each step's hypotheses are met by the outputs of the steps it uses: same ranges, same
  normalisation, no silently dropped condition.
- **Constants and parameters.** These propagate consistently. Recompute any arithmetic that combines them.
- **Versions.** Every result used is the frozen version that passed its check, not an earlier draft.
- **Cited results.** Others' results are cited correctly, and their exact hypotheses are satisfied. You do not
  re-prove them.
- **Main theorem.** It follows from the chain exactly as stated; nothing stronger is claimed.

RETURN WHEN: every edge of the dependency graph has a verdict.

{{COMMON_RULES}}

## SUMMARY (your final message)
- edges checked: <n>; failing edges: <edge: problem; which leaf/result must be reopened>
- version mismatches: <list or "none">
- verdict: CHAIN HOLDS | CHAIN BROKEN AT <edges>
