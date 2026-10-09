# Paper track, agent {{LABEL}}

{{TARGET_BLOCK}}

The final audit has passed. Write a paper a mathematician would enjoy reading, from the frozen package in
{{PACKAGE_DIR}}: MAIN.md, results/, cited.md, code/, certificates/, plus the pool for the history.

Extra instructions (venue style, length, toolchain): {{EXTRA}}

## Your task

Write LaTeX in {{PACKAGE_DIR}}/paper/. Structure:
1. **Introduction.** The problem, and the record history taken from the pool with correct attribution, including
   AI-assisted results. Then our result and what is new.
2. **Main theorem**, stated exactly as in MAIN.md.
3. **Overview of the method.** The idea before the details: where the gain comes from, and the binding constraint.
4. **Proofs.** Follow the dependency graph. Every theorem and lemma carries a comment `% package: RES-xx vN` or
   `% cited: P-xxx`, so the paper never drifts from what was audited.
5. **Computations.** What was computed, how it was made rigorous, and how to reproduce it (code and certificate
   paths).
6. **AI-use statement.** State plainly which parts were AI-generated or AI-assisted and how they were checked: one
   independent check per result, a final audit, and the formalisation status table, which the Lean track fills
   in.
7. References.

Readability matters. Motivate before computing, keep notation consistent, and add a figure or table where it
helps. If no TeX engine (latexmk, tectonic) is available, also {{TYPESETTING}}, and say so.

Do not introduce new mathematics or change any statement. If the package has a gap, report it.

RETURN WHEN: the full draft compiles (or renders), and every theorem is tagged with its package ID.

{{COMMON_RULES}}

## SUMMARY (your final message)
- files: <paths>; builds: <pdf/html/tex-only>
- package gaps found while writing: <list or "none">
- open TODOs for the user: <venue, author list, acknowledgements, ...>
