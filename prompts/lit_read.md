# Close reading, agent {{LABEL}}

Goal of the campaign, in the user's words: {{GOAL}}

{{TARGET_BLOCK}}

## Your reading list

{{EXTRA}}

## Your task

Read each source on your list closely. Write the notes back into the pool by adding an update card with the
SAME ID in {{SHARD_FILE}} (read: read, notes:, obstructions:). Later agents will rely on your notes INSTEAD of
re-reading the source, so make them self-contained:

- the main theorems, with their exact hypotheses, ranges and constants. Mismatched hypotheses are the most common
  way a borrowed tool fails;
- how the record or bound is assembled: which inputs feed which step, and where the binding constraint is;
- explicit obstructions or "this method cannot go beyond X" statements, with page or line;
- reusable code, data or certificates, with their location;
- the numbers needed to reproduce the record in a model (parameters, tables).

RETURN WHEN: every source on your list has notes that would let someone use its results without opening it.

{{COMMON_RULES}}

## SUMMARY (your final message)
- read: <IDs>
- binding constraint of the current record (one line): <...>
- obstructions recorded: <IDs + one line each>
- reusable code/data: <IDs + paths>
