# Closing: freeze (11), final audit (12), paper + Lean (13), delivery (14)

## Phase 11: freeze

The root is solved, or the user chose a ladder rung as the deliverable.

1. `result.py freeze`. This freezes every result that passed its check, at its current version. A later change
   needs `bump`, which unfreezes it, and that part of the audit must be redone.
2. Build `package/`:
   - **MAIN.md:**
     - the main theorem, exactly as it will be claimed;
     - the dependency graph, from the tree path leaves → root that actually carries the proof. Each edge reads
       "X is used in step Y of Z";
     - the list of frozen result IDs and versions.
   - **results/RES-xx.md:** each frozen result's full statement and proof (copied from its run file), plus its check
     report.
   - **cited.md:** every external result used, with its pool ID, exact statement, hypotheses, and where we verify
     those hypotheses.
   - **code/ and certificates/:** everything needed to reproduce the numerics, plus a README with build and run
     commands. No absolute paths into the campaign.
3. Log `stage: 11-freeze`.

## Phase 12: one full final audit

**Why this is not a second check.** Each piece has had its one check. The audit checks a different object: the
ASSEMBLED chain. Do the pieces fit? Are the hypotheses met by the actual outputs? Are the constants consistent? Are
the versions frozen? Do the numbers reproduce from scratch? Is the claim still new?

Launch three fresh agents in parallel. None of them took part in the campaign, and each works only from `package/`:

| label | kind | checks |
|---|---|---|
| AUD-logic | audit_logic | every dependency edge: hypotheses, constants, versions, cited results' hypotheses |
| AUD-num | audit_numerics | clean rebuild from `package/code`, all numbers reproduced, plus an independent checker for the headline certificate |
| AUD-lit | audit_lit | re-sweep for the exact claim and the record values in between, since the last pool sweep |

- **All pass:** go to phase 13.
- **A failure:**
  - send it back to the specific leaf or result named in the failure;
  - fix it; `result.py bump`; its one check; re-freeze;
  - re-audit only the affected part, using the dependency graph to see what depends on the fixed piece.
- **Scoop found:** tell the user at once.

## Phase 13: two parallel tracks

**Paper** (`--kind paper`, label PAPER):
- It writes `package/paper/`: readable LaTeX with motivation, an overview, proofs that follow the dependency graph,
  the computations, an AI-use statement, and the formalisation status table.
- Every theorem carries `% package: RES-xx vN` so the paper cannot drift from what was audited.
- After the draft, one "reader" agent reviews readability only (not correctness), as `--kind paper` with
  `--extra "readability review only"`.
- **Toolchain:** check for a TeX engine (latexmk, tectonic) first. If there is none:
  - ask the user to approve installing one (e.g. a portable tectonic); or
  - render HTML with the tool named in config `typesetting`, or Markdown with MathJax/KaTeX.

**Lean** (`--kind lean`, label LEAN):
- Lean 4 + Mathlib, in `package/lean/`, with the toolchain from config `lean_bin` (or PATH) and the Mathlib cache
  from config `mathlib_cache` (or `lake exe cache get`); make_prompt puts both into the lean prompt.
- **Trust base.**
  - Others' published theorems missing from Mathlib go in ONE `Axioms.lean`, each with its pool ID. This follows
    the usual practice for conditional formalisations of recent research results.
  - Our own results should be proved; where that is out of reach, use `sorry` with a stated gap, never `axiom`.
  - Report `#print axioms` and any `native_decide` use.
- **Memory.** Lean and Mathlib builds are memory-hungry, so give this agent its share of budget.toml (often the
  per-agent maximum).

The two tracks feed each other:
- Lean finds a gap in the exposition → the paper fixes it.
- Lean finds a gap in the MATHEMATICS → back to phase 12 for that part.
- The paper's formalisation table is filled from the Lean summary.

## Phase 14: delivery

Tell the user, in their language:
- the main theorem;
- the audit verdicts;
- the paper's location and build status;
- the Lean status: axioms list, remaining sorries;
- the ledger summary:
  - total tokens by kind;
  - kills at the ceiling gate;
  - runs marked knowable_in_advance;
  - false kills, if any were discovered.

Publishing, submitting (arXiv, journals, Tao's optimisation-constants repo, the Palomar registry) or posting
anything is the user's decision. Prepare the materials, and do not send them.

Log `stage: 14-delivered`, and add the campaign's lessons to the project notes for the skill's own evaluation.
