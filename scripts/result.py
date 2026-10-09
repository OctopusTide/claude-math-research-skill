"""Results registry: every positive result gets exactly ONE independent check per version.

result.py <dir> add   --title "..." --route R07 --statement "..." --value "..." --check-plan "referee: ..."
                      [--depends "RES-01, P-L0-004"]
result.py <dir> check RES-03 --by "main-thread: independent MC, 1e6 samples" --status passed|failed
                      (records a check done by the coordinator itself; refused if this version already has one)
result.py <dir> bump  RES-03 --why "constant c changed after referee fix"
                      (new version -> check slot reopens; dependents are listed so they can be re-examined)
result.py <dir> freeze [RES-01 RES-02 ...]   (phase 11: mark versions frozen; no args = all passed results)
"""
import argparse
import sys

import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works under python -I too
from rclib import Campaign, append_card, ids_in, now, set_fields, utf8_stdout


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    p.add_argument("--title", required=True)
    p.add_argument("--route", default="")
    p.add_argument("--statement", required=True)
    p.add_argument("--value", default="")
    p.add_argument("--check-plan", required=True, help="who/what will be the ONE independent check")
    p.add_argument("--depends", default="")
    p = sub.add_parser("check")
    p.add_argument("rid")
    p.add_argument("--by", required=True)
    p.add_argument("--status", required=True, choices=["passed", "failed"])
    p = sub.add_parser("bump")
    p.add_argument("rid")
    p.add_argument("--why", required=True)
    p = sub.add_parser("freeze")
    p.add_argument("rids", nargs="*")
    a = ap.parse_args()
    c = Campaign(a.dir)
    path = c.p("results.md")
    res = c.results()

    if a.cmd == "add":
        rid = c.next_id(path, "RES-", 2)
        append_card(path, rid, a.title, {
            "route": a.route, "version": "1", "statement": a.statement, "value": a.value,
            "depends_on": a.depends, "check_plan": a.check_plan, "check_status": "none", "check_by": "",
            "frozen": "no", "created": now()})
        print(f"registered {rid} v1; its one check: {a.check_plan}")
    elif a.cmd == "check":
        r = res.get(a.rid) or sys.exit(f"{a.rid} not found")
        if (r.get("check_status", "none") or "none").lower() != "none":
            sys.exit(f"REFUSED: {a.rid} v{r.get('version')} already has its check ({r.get('check_status')} by "
                 f"{r.get('check_by')}). One check per version.")
        set_fields(path, a.rid, {"check_status": a.status, "check_by": a.by, "check_ref": f"main-thread {now()}"})
        print(f"{a.rid}: check recorded ({a.status})")
    elif a.cmd == "bump":
        r = res.get(a.rid) or sys.exit(f"{a.rid} not found")
        v = int(r.get("version", "1") or 1) + 1
        hist = (r.get("history", "") + f"\nv{v - 1} -> v{v} {now()}: {a.why}").strip()
        set_fields(path, a.rid, {"version": str(v), "check_status": "none", "check_by": "", "check_ref": "",
                                 "frozen": "no", "history": hist})
        deps = [k for k, x in res.items() if a.rid in ids_in(x.get("depends_on", ""))]
        print(f"{a.rid} -> v{v}; check slot reopened."
              + (f" Dependents to re-examine: {', '.join(deps)}" if deps else ""))
    elif a.cmd == "freeze":
        ids = a.rids or [k for k, x in res.items() if x.get("check_status", "").lower() == "passed"]
        for rid in ids:
            r = res.get(rid)
            if not r:
                print(f"skip {rid}: not found")
                continue
            if r.get("check_status", "").lower() != "passed":
                print(f"skip {rid}: check_status={r.get('check_status')} (only passed results can be frozen)")
                continue
            set_fields(path, rid, {"frozen": f"yes (v{r.get('version', '1')}, {now()})"})
            print(f"froze {rid} v{r.get('version', '1')}")


if __name__ == "__main__":
    main()
