"""Print a campaign's current state (use after a restart or compaction to resume).

status.py <campaign dir>
"""
import sys
from collections import Counter

import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works under python -I too
from rclib import Campaign, barrier_convergence, propagate, utf8_stdout


def report(c: Campaign) -> None:
    m, t = c.meta, c.target
    b, src = c.budget()
    run = c.running()
    used = sum(float(r.get("memory_gb", 0) or 0) for r in run)
    print(f"Campaign {m.get('name', '?')}  stage={m.get('stage', '?')}  dir={c.dir}")
    print(f"Goal (verbatim): {m.get('goal_verbatim', '')}")
    print(f"Target: status={t.get('target_status', 'none')}  value={t.get('target_value', '')} "
          f"{t.get('unit', '')}  better={t.get('better', '')}  record={t.get('record_value', '')}")
    print(f"Budget ({src[-1]}): agents {len(run)}/{b['max_concurrent_agents']}, memory {used:g}/"
          f"{b['total_memory_gb']} GB, per agent <= {b['per_agent_memory_gb']} GB")
    for r in run:
        print(f"  running {r['_id']}: {r.get('kind')} {r.get('route') or r.get('result') or ''} "
              f"label={r.get('label')} mem={r.get('memory_gb')} since {r.get('started')}")
    routes = c.routes()
    if routes:
        st = Counter(r.get("status", "draft") for r in routes.values())
        vd = Counter(r.get("verdict", "pending") or "pending" for r in routes.values())
        print("Routes:", dict(st), "| verdicts:", dict(vd))
    res = c.results()
    if res:
        print("Results:")
        for rid, r in res.items():
            print(f"  {rid} v{r.get('version', '1')} check={r.get('check_status', 'none')} "
                  f"by={r.get('check_by', '')} frozen={r.get('frozen', 'no')} :: {r['_title']}")
    nodes = c.nodes()
    if nodes:
        states, _ = propagate(c)
        roots = [n for n, x in nodes.items() if x.get("parent", "-").strip() in ("", "-")]
        for r in roots:
            print(f"Tree root {r}: {states[r][0]} {states[r][1]}")
    for bar, cls in barrier_convergence(c):
        print(f"STOP-RULE SIGNAL: barrier {bar} blocked {len(cls)} method classes: {', '.join(sorted(cls))}")
    print(f"Barriers: {len(c.barriers())}   Ledger entries: {len(c.ledger())}")


if __name__ == "__main__":
    utf8_stdout()
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    report(Campaign(sys.argv[1]))
