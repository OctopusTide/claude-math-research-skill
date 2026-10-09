# Literature pool shards

Each agent writes ONLY its own shard here: lit_pool/<label>.md. merge_pool.py builds ../lit_pool.md from all of them.
Entry IDs are P-<label>-<n> (e.g. P-L0-012). To update an entry someone else created (verify it, add reading
notes), write a card with the SAME ID in your own shard containing only the fields you change. Your fields win
over the origin shard's.

```
Entry format (example; fenced blocks are ignored):

## P-L0-012 Author A (AI-assisted): constant improved to 1.214
- claim: proves c <= 1.214 via a new bilinear estimate and a refined weight
- source: https://example.edu/~author/notes/constant.pdf   (URL or exact location)
- type: personal-page preprint                            (journal | arXiv | personal-page | tracker | code | post | talk)
- date: 2026-01-04 (rev. 2026-01-18)
- relevance: target                                       (target | tool | background)
- status: rough                                           (rough | verified | wrong | irrelevant)
- found_by: L0
- verified_by:                                            (agent that opened the source and confirmed the claim)
- read: no                                                (no | skimmed | read)
- notes:                                                  (reading notes: key theorems WITH exact hypotheses, constants)
- obstructions:                                           (obstructions the source states explicitly, with location)
- artifacts:                                              (released construction / certificate / code / data: links, or "none found")
- nodes:                                                  (tree nodes this helps, once the tree exists)
- trigger:                                                (for on-demand finds: the question that made you look)
- local_copy:                                             (path under the project's sources/, if downloaded)
```

"Verified" means the source really says what the claim says (numbers, dates, attribution, hypotheses).
It does NOT mean we refereed the mathematics: others' results are used as given.
