# Lean formalisation track, agent {{LABEL}}

{{TARGET_BLOCK}}

The final audit has passed. Formalise the frozen package in {{PACKAGE_DIR}} (MAIN.md, results/, cited.md,
certificates/) in Lean 4 + Mathlib.

{{LEAN_TOOLCHAIN}} Pin the project to a Mathlib revision compatible with that Lean version, and use the prebuilt
cache rather than building Mathlib: building it from source takes hours and tens of GB.

Extra instructions: {{EXTRA}}

## Your task

Work in {{PACKAGE_DIR}}/lean/.

- **Axioms file.** Other people's published theorems that Mathlib lacks are stated as explicit `axiom`s in ONE
  file, Axioms.lean. Each carries a docstring with its pool ID, the paper, and the theorem number. Keep this list
  short and honest: it is the trust base.
- **Our results.** Our own new results (results/RES-xx) should be PROVED, not axiomatised, as far as feasible.
  Where a proof is out of reach, use `sorry` with a comment saying exactly what is missing. Never use an axiom for
  this.
- **Numerical certificates.** Check these by kernel-checkable computation where possible (`decide`, `norm_num`,
  verified interval arithmetic). If you use `native_decide`, say so, because it trusts the compiler.
- **Theorem statements** mirror the paper's, with the same package IDs in comments.

RETURN WHEN:
- the main theorem compiles with only the declared axioms and listed `sorry`s; or
- formalisation of some piece is blocked. In that case name the piece and what Mathlib lacks.

If the formalisation exposes a real gap in the mathematics, not just a missing library lemma, return
immediately and describe it. The coordinator sends it back to the final audit.

{{COMMON_RULES}}

## SUMMARY (your final message)
- builds: yes/no; `#print axioms MainTheorem` output: <list>
- axioms (others' theorems): <name: pool ID>
- sorries remaining: <name: what is missing>
- native_decide used: <where, or "no">
- mathematical gaps found: <list or "none">
- status table for the paper: <statement: proved / axiom / sorry>
