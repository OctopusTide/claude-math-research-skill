# Tool hunt, agent {{LABEL}}

{{TARGET_BLOCK}}

## Your node

{{NODE_CARD}}

Full tree: {{TREE_FILE}}

{{BARRIERS_BLOCK}}

Pool entries already attached to this node:
{{POOL_NOTES}}

## Your task

Find mathematical tools, from anywhere, that could close THIS node's gap.

Search with the node's exact statement, phrased in several vocabularies. The same object has different names in
different fields; for example a "character sum bound", a "discrepancy estimate" and an "equidistribution
statement" can all be one thing. Cover three groups:
- the same field, last 1-2 years: preprints, personal pages, talks;
- other fields with the same structure: other conjectures, combinatorics, dynamics, random matrices, coding
  theory, and so on;
- AI-math outputs: lab releases, Erdős-problem/AI wikis, evolve-style repos.

Mode for this hunt: {{EXTRA}}

For each candidate tool, add a pool entry in {{SHARD_FILE}} (relevance: tool, nodes: {{NODE_ID}}) with:
- its exact statement and hypotheses;
- what it would give when applied to this node, in the unified unit if you can estimate it;
- whether its hypotheses match our setting. If they do not, say exactly which one fails.

Do not attempt the proof. The coordinator turns good candidates into route cards, and those go through a
ceiling gate.

RETURN WHEN: each vocabulary and source group above has been searched and new searches only return known
entries.

{{COMMON_RULES}}

## SUMMARY (your final message)
- candidates: <ID: tool -> estimated effect on the node; hypotheses match yes/no/unclear>  (best first)
- rejected on hypotheses: <IDs + the failing hypothesis>
- for a barrier hunt: <has anyone got around it? how?>
