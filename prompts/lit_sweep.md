# Literature sweep (rough, wide), agent {{LABEL}}

Goal of the campaign, in the user's words: {{GOAL}}

{{TARGET_BLOCK}}

## Your task

Cast a wide net and dump what exists into the literature pool as rough entries. Breadth over accuracy: other
agents will verify each entry against its source and fill gaps, so do NOT read deeply and do NOT verify.

Cover:
- current records and their history, including who holds them, with what method, and when;
- the papers and posts behind those records;
- recent (last 2 years) work on the same problem and its direct sub-problems;
- AI-math outputs that touch it (lab releases, AlphaEvolve/EinsteinArena style repos, Erdős-problem trackers);
- known obstructions or "limits of the method" statements;
- released artifacts behind each record: constructions, certificates, code, data. Link them; later agents start
  from them.

Search the explicit target strings, not just topic words: the numbers, tuples and record values themselves
(the exact record value, the exact parameter tuple a result would need), as well as the problem's names in
other fields.

Titles and abstracts are not enough. A result can sit only in a paper's body, for example in a methods paper
(machine learning, optimisation, computer-assisted proof) whose abstract does not name the problem. The web
search tool summarises pages and is not a full-text index, and Google Scholar may be unreachable, so do this as a
**methods-paper sweep**:
1. Search for recent (last 12 months) computational- and AI-discovery papers IN GENERAL, without the problem's
   name: e.g. "certified computational discovery extremal", "neural network extremal constructions", "LLM-guided
   search mathematics", "evolutionary search new bounds", plus the arXiv listings of cs.LG, cs.AI, math.OC and
   stat with such words. Collect every paper that reports results on several unnamed or listed problems.
2. Open each one's full text (the arXiv HTML page, `arxiv.org/html/<id>`, or the PDF) and search the body for the
   problem's names and the target strings. Record a hit as a pool entry; record the paper as checked either way.
Also try Google Scholar / Semantic Scholar full-text queries for the target strings when they are reachable.

Sources:
- arXiv and journals, by title/abstract AND by full text;
- authors' personal and faculty pages (records are sometimes posted ONLY there);
- GitHub;
- trackers and wikis;
- X/Mathstodon and blogs;
- lab announcements.

Extra instructions: {{EXTRA}}

Write each find as one entry in {{SHARD_FILE}} with status: rough, found_by: {{LABEL}}, and a one-line claim,
source, type, date, relevance (target/tool/background) and artifacts (links to released constructions or code,
or "none found"). Aim for coverage: dozens of entries is normal.

RETURN WHEN: you have covered every source class above for the target strings and the main sub-problems, or you
are only finding entries already in your shard.

{{COMMON_RULES}}

## SUMMARY (your final message)
- entries: <count> (target <n>, tool <n>, background <n>)
- possible scoop / record changes: <IDs + one line each, or "none seen">
- released artifacts for the current record: <ID: link, or "none found">
- source classes covered (say which were searched by full text): <list>; not reachable: <list>
- suggested split for verifiers: <how to divide the rough entries by source class>
