"""Show the AND/OR problem tree with states propagated up from the route cards, plus stop-rule signals.

tree_status.py <campaign dir>

A route counts as solved when status is done/solved (and outcome is not negative), blocked when
status is killed/blocked (or done with outcome negative), otherwise open.
OR node: solved if any child solved; blocked if every child blocked.
AND node: solved if every child solved; blocked if any child blocked.
"""
import sys

import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works under python -I too
from rclib import Campaign, barrier_convergence, propagate, route_state, utf8_stdout

MARK = {"solved": "✔", "blocked": "✘", "open": "·"}


def main():
    utf8_stdout()
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    c = Campaign(sys.argv[1])
    nodes, routes = c.nodes(), c.routes()
    if not nodes:
        print("tree.md has no nodes yet")
        return
    states, kids = propagate(c)

    def show(nid, depth):
        n = nodes[nid]
        s, why = states[nid]
        print(f"{'  ' * depth}{MARK[s]} {nid} [{n.get('type', 'OR').upper()}] {n['_title']}"
              f"  need: {n.get('needed', '')}  {('(' + why + ')') if why and s != 'open' else ''}")
        for kind, x in kids[nid]:
            if kind == "node":
                show(x, depth + 1)
            else:
                r = routes[x]
                rs = route_state(r)
                extra = f" blocked_by {r.get('blocked_by')}" if r.get("blocked_by") else ""
                print(f"{'  ' * (depth + 1)}{MARK[rs]} {x} <{r.get('method_class', '?')}> "
                      f"{r.get('status', 'draft')}/{r.get('verdict', 'pending') or 'pending'}{extra} — {r['_title']}")

    roots = [n for n, x in nodes.items() if x.get("parent", "-").strip() in ("", "-") or x["parent"] not in nodes]
    for r in roots:
        show(r, 0)
    orphans = [rid for rid, r in routes.items() if r.get("node", "").strip() not in nodes]
    if orphans:
        print("routes not attached to a tree node:", ", ".join(orphans))
    for r in roots:
        if states[r][0] == "blocked":
            print(f"\nSTOP RULE: root {r} is blocked. Report to the user what is still missing, naming the "
                  f"blocked leaves and their barriers. Do not launch more attacks on this path without their OK.")
        if states[r][0] == "solved":
            print(f"\nROOT {r} SOLVED: move to phase 11 (freeze).")
    for bar, cls in barrier_convergence(c):
        print(f"STOP-RULE SIGNAL: barrier {bar} has blocked {len(cls)} independent method classes "
              f"({', '.join(sorted(cls))}) -> report it to the user as conjecture-strength.")


if __name__ == "__main__":
    main()
