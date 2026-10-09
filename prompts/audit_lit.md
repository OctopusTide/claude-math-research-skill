# Final audit — literature re-sweep before the claim, agent {{LABEL}}

{{TARGET_BLOCK}}

Main claim we are about to make: see {{PACKAGE_DIR}}/MAIN.md.
The campaign's literature pool (lit_pool.md) was built earlier. Your job is to catch anything that appeared, or
was missed, since then.

Extra instructions (date of the last sweep, etc.): {{EXTRA}}

## Your task

Search for the explicit claim: the exact number, tuple or bound, and the record values between the old record
and ours. Cover:
- arXiv and journals;
- authors' personal and faculty pages, especially everyone in the pool's target entries;
- trackers and wikis;
- GitHub;
- X/Mathstodon and blogs;
- lab announcements.

Open every plausible hit. Add finds to {{SHARD_FILE}}.

Answer three questions:
- Has anyone already published or posted this claim, or a stronger one?
- Has the record moved since the pool was built?
- Is any cited result retracted or corrected?

RETURN WHEN: all source classes have been searched for the claim strings.

{{COMMON_RULES}}

## SUMMARY (your final message)
- prior or concurrent claims of the same or a stronger result: <IDs + dates, or "none found">
- record changes since the last sweep: <...>
- retractions or corrections of cited results: <...>
- verdict: CLAIM IS NEW | SCOOPED BY <ID> | PARTLY ANTICIPATED BY <ID>
