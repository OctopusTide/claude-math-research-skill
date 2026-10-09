"""Close a ledger entry when its agent returns (frees its budget slot).

finish_run.py <campaign dir> <ledger id> --outcome "<one line>"
              [--tokens N] [--minutes M] [--knowable yes|no|partly]
              [--route-status draft|queued|done|blocked|killed|shelved] [--route-outcome positive|negative|partial]
              [--blocked-by B03] [--result-check passed|failed]

--knowable records whether the outcome could have been known before launch (evaluation data for the skill).
"""
import argparse
import datetime

import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works under python -I too
from rclib import Campaign, now, set_fields, utf8_stdout


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("lid")
    ap.add_argument("--outcome", required=True)
    ap.add_argument("--tokens", type=int)
    ap.add_argument("--minutes", type=float)
    ap.add_argument("--knowable", choices=["yes", "no", "partly"])
    ap.add_argument("--route-status")
    ap.add_argument("--route-outcome", choices=["positive", "negative", "partial"])
    ap.add_argument("--blocked-by")
    ap.add_argument("--result-check", choices=["passed", "failed"])
    a = ap.parse_args()
    c = Campaign(a.dir)
    L = c.ledger().get(a.lid)
    if not L:
        raise SystemExit(f"{a.lid} not in ledger.md")
    upd = {"status": "done", "finished": now(), "outcome": a.outcome}
    if a.minutes is None:
        try:
            t0 = datetime.datetime.strptime(L.get("started", ""), "%Y-%m-%d %H:%M")
            a.minutes = round((datetime.datetime.now() - t0).total_seconds() / 60, 1)
        except ValueError:
            pass
    if a.minutes is not None:
        upd["minutes"] = f"{a.minutes:g}"
    if a.tokens is not None:
        upd["tokens"] = str(a.tokens)
    if a.knowable:
        upd["knowable_in_advance"] = a.knowable
    set_fields(c.p("ledger.md"), a.lid, upd)
    route = L.get("route", "").strip()
    if route and (a.route_status or a.route_outcome or a.blocked_by):
        r = {}
        if a.route_status:
            r["status"] = a.route_status
        if a.route_outcome:
            r["outcome"] = a.route_outcome
        if a.blocked_by:
            r["blocked_by"] = a.blocked_by
        set_fields(c.p("routes.md"), route, r)
    res = L.get("result", "").strip()
    if res and a.result_check:
        set_fields(c.p("results.md"), res, {"check_status": a.result_check})
    print(f"closed {a.lid} ({L.get('kind')} {L.get('label')}); {len(c.running())} agents still running")


if __name__ == "__main__":
    main()
