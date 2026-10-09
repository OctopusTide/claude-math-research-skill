# Final audit — numerics from a clean build, agent {{LABEL}}

{{TARGET_BLOCK}}

You are a fresh reader. Work ONLY from the frozen package in {{PACKAGE_DIR}}: MAIN.md, results/, code/,
certificates/.

Extra instructions: {{EXTRA}}

## Your task

1. **Clean rebuild.** Build the package's code in a NEW empty directory, from source only, following its README.
   Run it, and confirm that every number in MAIN.md and the results files is reproduced exactly: rigorous bounds
   with their rounding, tuples/objects passing their checkers.
2. **Independent check.** Write your own small independent checker for the headline certificate(s): the final
   inequality, the admissibility or validity of the object, the key bound. Do not reuse the package's checker.
3. **Package defects.** List anything missing for a stranger to reproduce: undeclared inputs, hard-coded paths,
   floating-point where a rigorous bound is claimed, nondeterminism.

RETURN WHEN: the headline numbers are reproduced (or shown not to be), and the independent checker has run.

{{COMMON_RULES}}

## SUMMARY (your final message)
- rebuilt from clean: yes/no (<problems>)
- reproduced: <number: ok/mismatch (got ...)>
- independent checker: <what it checks; result>
- package defects: <list or "none">
- verdict: NUMERICS HOLD | FAIL AT <items>
