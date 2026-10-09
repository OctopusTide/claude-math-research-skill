## Ground rules for every agent in this campaign

- Campaign folder: {{CAMPAIGN_DIR}}. CAMPAIGN.md holds the goal and the TARGET card; lit_pool.md is the shared
  literature pool (index first, then the entries you need). Look things up in the pool BEFORE searching or
  re-reading a source; if the pool already has reading notes, use them.
- Write only to your own files: your run file {{RUN_FILE}} and, if you add literature, your pool shard
  {{SHARD_FILE}} (entry IDs {{SHARD_PREFIX}}1, {{SHARD_PREFIX}}2, ...; format in lit_pool/README.md). Never edit
  CAMPAIGN.md, tree.md, routes.md, barriers.md, results.md, ledger.md or other agents' files: the coordinator
  merges.
- When you hit a question the pool cannot answer, search for it (arXiv, journals, authors' personal and faculty
  pages, GitHub, trackers, X/Mathstodon, blogs), open every plausible hit, and add what you find to your shard
  with `trigger:` naming the question.
- Other people's results (papers, preprints, posted AI-assisted proofs) are inputs: use them as stated; do not
  audit or re-prove them. Do check that their exact hypotheses match how you use them, and say so.
- {{MEMORY_CAP}}
  Kill every process you started before you return.
- There is no time limit. Return as soon as one of your RETURN WHEN conditions holds. Do not grind: if three
  genuinely different approaches fail on the same sub-step, that is itself a return condition. Report it with
  what you tried.
- Keep a running log in {{RUN_FILE}} as you work (decisions, numbers, code paths), so nothing is lost if you are
  interrupted.
- Numbers: give each one in the campaign's unified unit ({{UNIT}}) where it applies, and say how you got it:
  computed (code path), quoted (pool ID + location) or estimated.
- Negative findings: phrase them as "what is still missing", naming the obstruction and the evidence. Do not
  write "impossible" unless you proved it.
- If a tool refuses to write a file, put the content in your final message instead. Do not work around the
  refusal with another tool.
- Your final message is ONLY the SUMMARY block from your task, at most 25 lines. The full story stays in your run
  file. The coordinator reads the summary, not a narrative.
